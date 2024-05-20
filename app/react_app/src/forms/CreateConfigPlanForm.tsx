import React, { useState, useEffect } from "react";
import axios, { AxiosResponse } from "axios";
import dayjs, { Dayjs } from "dayjs";
import { Stack } from "@mui/material";
import { ThemeProvider } from "@emotion/react";
import TextField from "@mui/material/TextField";
import { createUniqueAndSort, theme } from "../Utils";
import { AutocompleteButton, SubmitClearButton } from "../buttons/Buttons";
import { IButton, ISelectList } from "../buttons/ButtonsUtils";
import {
    CatalogDetails,
    ICatalogDetailsResponse,
    IFormDetails,
    IOSSelfQueryResponse,
    IOSTypeResponse,
    OSSelfQuery,
    ICIName,
} from "./FormUtils";
import DatePickerButton from "../buttons/DatePickers";
import EnhancedTable from "../table/EnhancedTable";
import { ITableColumn, ITableRow } from "../table/TableUtils";

interface IHead extends ITableRow {
    cisid?: string;
    host?: string;
    checkbox: JSX.Element;
    selected: string;
}

interface IBody extends ITableRow {
    cisid?: string;
    host?: string;
    handleClick: (e: React.MouseEvent<HTMLElement>) => void;
}

interface FormHeadColumn extends ITableColumn<IHead> {
    align?: "right";
    format?: (value: any) => string;
}

interface FormBodyColumn extends ITableColumn<IBody> {
    align?: "right";
    format?: (value: any) => string;
}

interface CINameColumn extends ITableColumn<ICIName> {
    align?: "right";
    format?: (value: any) => string;
}

let ciNameColumns: CINameColumn[] = [
    { id: "hostname", label: "Hostname", width: "10%" },
    { id: "SessionID", label: "SessionID", width: "10%" },
    { id: "ciUUID", label: "CI UUID", width: "15%" },
];

export default function CreateConfigPlanForm<T extends IFormDetails>() {
    // options
    const [CITypeOptions, setCITypeOptions] = useState<ISelectList<IButton>>({
        options: [],
    });
    const [benchmarkOptions, setBenchmarkOptions] = useState<ISelectList<IButton>>({ options: [] });
    const [hostnameOptions, setHostnameOptions] = useState<ISelectList<IButton>>({
        options: [],
    });

    // table
    const [sessionIDPayload, setSessionIDPayload] = useState<object>({});
    const [selectedSessionID, setSelectedSessionID] = useState<string[]>([]);
    const [OSType, setOSType] = useState<IOSTypeResponse<T>>();
    const [startTime, setStartTime] = useState<Dayjs>(dayjs(""));
    const [endTime, setEndTime] = useState<Dayjs>(dayjs(""));
    const [selectedCIType, setSelectedCIType] = useState<string>("");
    const [selectedCrRequest, setSelectedCrRequest] = useState<string>("");
    const [selectedCISBenchmark, setSelectedCISBenchmark] = useState<string>("");
    const [selectedHostname, setSelectedHostname] = useState<string>("");
    const [uuidArray, setUUIDArray] = useState<string[]>([]);

    const [isEmptyTable, setIsEmptyTable] = useState<boolean>(true);

    const [msg, setMsg] = useState<string>("");

    const formSessionIDColumnHead: FormHeadColumn[] = [
        { id: "checkbox", label: <></>, width: "10%", headExcluedSort: true },
        { id: "cisid", label: "Session ID", width: "40%", headExcluedSort: true },
        {
            id: "selected",
            label: selectedSessionID.length.toString() + " Selected",
            width: "50%",
            headExcluedSort: true,
        },
    ];

    const formSessionIDColumnBody: FormBodyColumn[] = [{ id: "cisid", label: "Session ID", width: "100%" }];

    useEffect(() => {
        setMsg("Please wait while we collect data for you");
        axios.get("/services/form/os_type/").then((response: AxiosResponse) => {
            setOSType(response.data);
        });
    }, []);

    useEffect(() => {
        setCITypeOptions({
            options: OSType ? OSType.data.os_data : [],
        });
        setMsg("");
    }, [OSType]);

    // Getting CIS Benchmark
    useEffect(() => {
        resetSelected();
        if (selectedCIType !== "") {
            setMsg("Please wait as we collect data for you");
            axios
                .post("/services/form/os_self_query/", {
                    os_type: selectedCIType,
                    selected_fields: ["benchmark"],
                    filter_fields: {},
                })
                .then((response: AxiosResponse) => {
                    const selfQueryRes: IOSSelfQueryResponse<IFormDetails> = response.data;
                    const data: OSSelfQuery = selfQueryRes.data;
                    setBenchmarkOptions({
                        options: createUniqueAndSort(
                            data.selected_data.hasOwnProperty("benchmark") ? data.selected_data["benchmark"] : [],
                        ),
                    });

                    setMsg("");
                })
                .catch(() => {
                    setMsg("Something went wrong with collect data for the Device Type");
                });
        }
    }, [selectedCIType]);

    // Getting hostname
    useEffect(() => {
        if (selectedCISBenchmark !== "") {
            setMsg("Please wait as we collect data for you");
            setSelectedHostname("");
            axios
                .post("/services/form/os_self_query/", {
                    os_type: selectedCIType,
                    selected_fields: ["host"],
                    filter_fields: { benchmark: [selectedCISBenchmark] },
                })
                .then((response: AxiosResponse) => {
                    const selfQueryRes: IOSSelfQueryResponse<IFormDetails> = response.data;
                    const data: OSSelfQuery = selfQueryRes.data;
                    setHostnameOptions({
                        options: createUniqueAndSort(
                            data.selected_data.hasOwnProperty("host") ? data.selected_data["host"] : [],
                        ),
                    });

                    setMsg("");
                })
                .catch(() => {
                    setMsg("Something went wrong with collecting data from CIS Benchmark");
                });
        }
    }, [selectedCISBenchmark]);

    // Getting Section ID
    useEffect(() => {
        if (selectedCISBenchmark !== "" && selectedCIType !== "" && selectedHostname !== "") {
            setIsEmptyTable(false);
        }

        const filter_field: { [key: string]: string[] } = {};
        if (selectedHostname !== "") {
            filter_field["host"] = [selectedHostname];
        }

        setSessionIDPayload({
            os_type: selectedCIType,
            selected_fields: ["cisid"],
            filter_fields: filter_field,
        });
    }, [selectedHostname]);

    const handleClickForTableBodySessionID = (obj: IBody, selectedArray: string[], setSelectedArray: Function) => {
        if (obj.cisid) {
            if (selectedArray.includes(obj.cisid)) {
                setSelectedArray(selectedArray.filter((name: string) => name !== obj.cisid));
            } else {
                selectedArray.push(obj.cisid);
                setSelectedArray([...selectedArray]);
            }
        }
    };

    const renderSingleOrMultipleHost = (
        <AutocompleteButton<IButton>
            header="Hostname"
            value={selectedHostname}
            setValue={setSelectedHostname}
            list={hostnameOptions}
        />
    );

    const renderSessionID = (
        <EnhancedTable<IHead, IBody>
            api={"/services/form/os_self_query/"}
            requestType="post"
            payload={sessionIDPayload}
            columnsHead={formSessionIDColumnHead}
            columnsBody={formSessionIDColumnBody}
            defaultOrderBy={"cisid"}
            handleClick={handleClickForTableBodySessionID}
            selectedObj={selectedSessionID}
            setSelectedObj={setSelectedSessionID}
            selectedObjName="cisid"
            isEmpty={isEmptyTable}
        />
    );

    const handleSubmit = async () => {
        if (
            !selectedSessionID.length ||
            !selectedCIType.length ||
            !selectedCrRequest.length ||
            !startTime ||
            !endTime ||
            !selectedCISBenchmark ||
            !selectedHostname.length
        ) {
            setMsg("Please Input in each field");
            return;
        }

        setMsg("Sending in Job, Please wait");
        let selfQueryPayload: { [key: string]: any } = {};
        let cataglogParam: string = "";
        switch (selectedCIType) {
            case "Network Device":
                selfQueryPayload = {
                    os_type: selectedCIType,
                    selected_fields: ["host", "uuid", "cisid"],
                    filter_fields: { host: [selectedHostname] },
                };
                cataglogParam = "Resolve Launch job";
                break;

            default: // windows & linux
                selfQueryPayload = {
                    os_type: selectedCIType,
                    selected_fields: ["host", "cisid"],
                    filter_fields: { host: [selectedHostname] },
                };
                cataglogParam = "Resolve Launch job";
                break;
        }

        let selfQueryResponse: { [keys: string]: any } = {};
        await axios
            .post("/services/form/os_self_query/", selfQueryPayload)
            .then((response: AxiosResponse) => {
                selfQueryResponse = response;
            })
            .catch(() => {
                setMsg("Something went wrong with collecting Host Data");
                return;
            });

        let catalogResponse: { [keys: string]: any } = {};
        await axios
            .get("/services/form/catalog_details/", {
                params: { catalog_name: cataglogParam },
            })
            .then((response: AxiosResponse) => {
                catalogResponse = response;
            })
            .catch(() => {
                setMsg("Something went wrong with collecting the Catalog Details");
                return;
            });

        const selfQueryRes: IOSSelfQueryResponse<IFormDetails> = selfQueryResponse.data;
        const data: OSSelfQuery = selfQueryRes.data;

        const myCatalogResponse: ICatalogDetailsResponse<IFormDetails> = catalogResponse.data;
        const catalogData: CatalogDetails = myCatalogResponse.data;

        const hostArray: Array<string> = "host" in data.selected_data ? (data.selected_data.host as string[]) : [];
        const cisidArray: Array<string> = "cisid" in data.selected_data ? data.selected_data.cisid : [];
        const payloadCiName: { [key: string]: string }[] = [];
        if (selectedCIType === "Network Device") {
            const uuidArray: Array<string> = "uuid" in data.selected_data ? data.selected_data.uuid : [];

            let selfQueryFeatureRes: { [keys: string]: any } = {};
            const cleanedSelectedCIName: string[] = [];
            // to remove whitespace
            selectedSessionID.forEach((value) => {
                cleanedSelectedCIName.push(value.trim());
            });
            await axios
                .post("/services/form/os_self_query/", {
                    os_type: "Network Device",
                    selected_fields: ["feature_name", "feature_uuid"],
                    filter_fields: {
                        benchmark: [selectedCISBenchmark],
                        feature_name: cleanedSelectedCIName,
                    },
                })
                .then((response: AxiosResponse) => {
                    selfQueryFeatureRes = response.data;
                })
                .catch(() => {
                    setMsg("Something went wrong with collecting Host Data");
                    return;
                });
            const featureData: OSSelfQuery = selfQueryFeatureRes.data;
            if (
                "selected_data" in featureData &&
                "feature_name" in featureData["selected_data"] &&
                "feature_uuid" in featureData["selected_data"]
            ) {
                payloadCiName.push({
                    hostname: uuidArray.length == hostArray.length && hostArray[0] ? hostArray[0] : "",
                    featurename: `"${featureData["selected_data"]["feature_name"].join('","')}"`,
                    featureUUID: `"${featureData["selected_data"]["feature_uuid"].join('","')}"`,
                    hostUUID: uuidArray.length == hostArray.length && uuidArray[0] ? uuidArray[0] : "",
                });
            }
        } else {
            payloadCiName.push({
                hostname: selectedHostname,
                SessionID: selectedSessionID.join(),
            });
        }

        const payload: { [key: string]: any } = {
            SessionID: "0",
            requestType: "cm:configplan creation for " + selectedCIType,
            request_control_id: selectedCrRequest,
            ciType: selectedCIType,
            plan_start: startTime,
            plan_end: endTime,
            ciName: payloadCiName,
            CISBenchmark: selectedCISBenchmark,
        };
        if (selectedCIType === "Network Device") {
            let configplan_uuid = "";
            await axios
                .post("/services/form/os_self_query/", {
                    os_type: "Network Device",
                    selected_fields: ["sp_configplan_name", "sp_configplan_uuid"],
                    filter_fields: {
                        configplan_name: "Generate Config Plans",
                    },
                })
                .then((response: AxiosResponse) => {
                    configplan_uuid = response.data.data["selected_data"]["sp_configplan_uuid"][0];
                })
                .catch(() => {
                    setMsg("Something went wrong with collecting configplan_uuid");
                    return;
                });
            let nbcrUUID = "";
            await axios
                .post("/services/form/os_self_query/", {
                    os_type: "Network Device",
                    selected_fields: ["configplan_nbcr_approved_uuid"],
                    filter_fields: {},
                })
                .then((response: AxiosResponse) => {
                    nbcrUUID = response.data.data["selected_data"]["configplan_nbcr_approved_uuid"][0];
                })
                .catch(() => {
                    setMsg("Something went wrong with collecting configplan_nbcr_approved_uuid");
                    return;
                });
            payload["nbcr_approved_uuid"] = nbcrUUID;
            payload["generate_configplan_uuid"] = configplan_uuid;
        }

        await axios
            .post("/services/form/launch_job/", {
                template_id: catalogData.catalog_template_id,
                launch_url: catalogData.catalog_launch_url,
                payload: payload,
            })
            .then((jobResponse: AxiosResponse) => {
                setMsg("JobID: " + jobResponse.data.job_id + "\nStatus: " + jobResponse.data.status);
            })
            .catch(() => {
                setMsg("Something went wrong with job sending");
            });
    };

    const resetSelected = (): void => {
        setSelectedCrRequest("");
        setSelectedCISBenchmark("");
        setSelectedHostname("");
        setSelectedSessionID([]);
        setUUIDArray([]);
        setStartTime(dayjs(""));
        setEndTime(dayjs(""));
        setBenchmarkOptions({ options: [] });
        setHostnameOptions({ options: [] });
        setIsEmptyTable(true);
    };

    return (
        <ThemeProvider theme={theme}>
            <h3> Create Config Plan </h3>
            <Stack direction="row" useFlexGap flexWrap="wrap" spacing={{ xs: 1, sm: 2 }}>
                <AutocompleteButton<IButton>
                    header="CI Type"
                    value={selectedCIType}
                    setValue={setSelectedCIType}
                    list={CITypeOptions}
                />
                <TextField
                    label="CR Requester"
                    value={selectedCrRequest}
                    onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                        setSelectedCrRequest(event.target.value);
                    }}
                />
                <DatePickerButton
                    label="CR Start Time"
                    value={startTime}
                    onChange={(newValue: Dayjs) => {
                        if (newValue.isBefore(Date.now())) {
                            setMsg("Start Time should not be before current time");
                            return;
                        }
                        setStartTime(newValue);
                        setMsg("");
                    }}
                />
                <DatePickerButton
                    label="CR End Time"
                    value={endTime}
                    onChange={(newValue: Dayjs) => {
                        if (newValue.isBefore(startTime)) {
                            setMsg("End Time is before the Start Time, please set the End time to be in the future");
                            return;
                        }

                        setEndTime(newValue);
                        setMsg("");
                    }}
                />
                <AutocompleteButton<IButton>
                    header="CIS Benchmark"
                    value={selectedCISBenchmark}
                    setValue={setSelectedCISBenchmark}
                    list={benchmarkOptions}
                />
                {renderSingleOrMultipleHost}
                {renderSessionID}
            </Stack>
            {msg !== "" && <h5>{msg}</h5>}
            <br></br>
            <SubmitClearButton
                handleClear={() => {
                    resetSelected();
                    setSelectedCIType("");
                }}
                handleSubmit={handleSubmit}
            />
        </ThemeProvider>
    );
}
