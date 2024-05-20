import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom/client";
import axios, { AxiosResponse } from "axios";

import { IButton, ISelectList } from "./buttons/ButtonsUtils";
import { AutocompleteButton, SubmitClearButton } from "./buttons/Buttons";
import { ISidebar, SidebarItem } from "./sidebar/SidebarUtils";
// Icons input
import ChecklistIcon from "@mui/icons-material/Checklist";
import ArrowRightIcon from "@mui/icons-material/ArrowRight";
import ArrowLeftIcon from "@mui/icons-material/ArrowLeft";

import Sidebar from "./sidebar/Sidebar";
import { Button, Stack, ThemeProvider } from "@mui/material";
import { createUniqueAndSort, theme } from "./Utils";
import { ITableColumn, ITableRow } from "./table/TableUtils";
import EnhancedTable from "./table/EnhancedTable";
import {
    CatalogDetails,
    ICatalogDetailsResponse,
    IFormDetails,
    IOSSelfQueryResponse,
    IOSTypeResponse,
    OSSelfQuery,
} from "./forms/FormUtils";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

interface IHostBody extends ITableRow {
    host: string;
    handleClick: (e: React.MouseEvent<HTMLElement>) => void;
}
interface FormHostBodyColumn extends ITableColumn<IHostBody> {
    align?: "right";
    format?: (value: any) => string;
}

interface IHostHead extends ITableRow {
    host: string;
    checkbox: JSX.Element;
    selected: string;
}
interface FormHostHeadColumn extends ITableColumn<IHostHead> {
    align?: "right";
    format?: (value: any) => string;
}

export default function Form<T extends IFormDetails>() {
    // options
    const [deviceTypeOptions, setDeviceTypeOptions] = useState<ISelectList<IButton>>({ options: [] });
    const [benchmarkOptions, setBenchmarkOptions] = useState<ISelectList<IButton>>({ options: [] });
    // const [platformOptions, setPlatformOptions] = useState<ISelectList<IButton>>({ options: [] });

    const [osTypeResponse, setOsTypeResponse] = useState<IOSTypeResponse<T>>();
    // dropdown
    const [selectedDeviceType, setSelectedDeviceType] = useState<string>("");
    const [selectedBenchmark, setSelectedBenchmark] = useState<string>("");
    const [selectedPlatform, setSelectedPlatform] = useState<string>("");
    // table
    const [hostPayload, setHostPayload] = useState<object>({});
    const [subHostPayload, setSubHostPayload] = useState<object>({});
    const [selectedHost, setSelectedHost] = useState<string[]>([]);
    const [selectedSubHost, setSelectedSubHost] = useState<string[]>([]);
    const [allSubHost, setAllSubHost] = useState<string[]>([]);
    // Sidebar Items
    const [sidebarItems, setSidebarItems] = useState<SidebarItem<ISidebar>[]>([]);
    const [isSubHostTableEmpty, setIsSubHostTableEmpty] = useState<boolean>(true);

    const [msg, setMsg] = useState<string>("");

    const formHostColumnHead: FormHostHeadColumn[] = [
        { id: "checkbox", label: <></>, width: "5%", headExcluedSort: true },
        { id: "host", label: "Host", width: "40%", headExcluedSort: true },
        {
            id: "selected",
            label: selectedHost.length.toString() + " Selected",
            width: "50%",
            headExcluedSort: true,
        },
    ];

    const formSubHostColumnHead: FormHostHeadColumn[] = [
        { id: "checkbox", label: <></>, width: "10%", headExcluedSort: true },
        { id: "host", label: "Submitting Host", width: "40%", headExcluedSort: true },
        {
            id: "selected",
            label: selectedSubHost.length.toString() + " Selected",
            width: "50%",
            headExcluedSort: true,
        },
    ];
    const formHostColumnBody: FormHostBodyColumn[] = [{ id: "host", label: "Host", width: "100%" }];

    const handleMoveLeft = () => {
        let filteredArray: string[] = [];
        if ("filter_fields" in subHostPayload && "host" in (subHostPayload["filter_fields"] as object)) {
            const filter_field: object = subHostPayload["filter_fields"] as object;
            const host_array: string[] = "host" in filter_field ? (filter_field["host"] as string[]) : [];
            filteredArray = host_array.filter((site: string) => !selectedSubHost.includes(site));
        }
        if (!filteredArray.length) {
            setIsSubHostTableEmpty(true);
            setAllSubHost([]);
        }
        setSelectedSubHost([]);
        setSubHostPayload({
            os_type: selectedDeviceType,
            selected_fields: ["host"],
            filter_fields: { host: filteredArray, benchmark: [selectedBenchmark] },
        });
    };
    const handleMoveRight = () => {
        if (selectedHost.length) {
            let filteredArray: string[] = [...selectedHost];
            if (
                "filter_fields" in subHostPayload &&
                "host" in (subHostPayload.filter_fields as { [key: string]: string[] })
            ) {
                filteredArray = filteredArray.concat(
                    (subHostPayload.filter_fields as { [key: string]: string[] })["host"].filter(
                        (host: string) => !filteredArray.includes(host),
                    ),
                );
            }
            setSubHostPayload({
                os_type: selectedDeviceType,
                selected_fields: ["host"],
                filter_fields: { host: filteredArray, benchmark: [selectedBenchmark] }, // to make it so it cannot find anything
            });
            setSelectedHost([]);
            setIsSubHostTableEmpty(false);
        } else {
            setIsSubHostTableEmpty(true);
        }
    };

    // getting os type reponse at the start - not sure y need to save guard to get the
    useEffect(() => {
        setMsg("Please wait as we collect data for you");
        axios.get("/services/form/os_type/").then((getresponse: AxiosResponse) => {
            setOsTypeResponse(getresponse.data);
        });
    }, []);
    // with the response set it in our OSType Option
    useEffect(() => {
        if (osTypeResponse && osTypeResponse.data.os_data.length) {
            setDeviceTypeOptions({
                options: osTypeResponse ? osTypeResponse.data.os_data : [],
            });
            setMsg("");
        }
    }, [osTypeResponse]);
    // when the os type change it the change the filtered response
    useEffect(() => {
        // when not empty get respons
        resetSelected();
        if (selectedDeviceType !== "") {
            setMsg("Please wait as we collect data for you");
            const selected_fields: string[] = ["region", "country", "site", "benchmark"];
            axios
                .post("/services/form/os_self_query/", {
                    os_type: selectedDeviceType,
                    selected_fields: selected_fields,
                    filter_fields: {},
                })
                .then((response: AxiosResponse) => {
                    const selfQueryRes: IOSSelfQueryResponse<IFormDetails> = response.data;
                    const data: OSSelfQuery = selfQueryRes.data;
                    const sidebarList: SidebarItem<ISidebar>[] = [
                        { name: "Region", icon: ChecklistIcon, children: [] },
                        { name: "Country", icon: ChecklistIcon, children: [] },
                        { name: "Site", icon: ChecklistIcon, children: [] },
                    ];
                    sidebarList.forEach((sidebar: SidebarItem<IFormDetails>) => {
                        const name: string = sidebar.name.toLowerCase();
                        const uniques: string[] = createUniqueAndSort(
                            data.selected_data.hasOwnProperty(name) ? data.selected_data[name] : [],
                        );
                        uniques.forEach((item: string) => {
                            sidebar?.children?.push({ name: item });
                        });
                    });
                    const uniques: string[] = createUniqueAndSort(
                        data.selected_data.hasOwnProperty("benchmark") ? data.selected_data["benchmark"] : [],
                    );
                    setBenchmarkOptions({ options: uniques });

                    setSidebarItems(sidebarList);
                    setMsg("");
                })
                .catch(() => {
                    setMsg("Something went wrong with collect data for the Device Type");
                });
        }
    }, [selectedDeviceType]);

    useEffect(() => {
        const filter_field: { [key: string]: string[] } = {};
        sidebarItems.forEach((value: SidebarItem<ISidebar>) => {
            value.children?.forEach((childValue: SidebarItem<ISidebar>) => {
                if (childValue.selected) {
                    if (!filter_field[value.name.toLocaleLowerCase()])
                        filter_field[value.name.toLocaleLowerCase()] = [];
                    filter_field[value.name.toLocaleLowerCase()].push(childValue.name);
                }
            });
        });
        if (selectedBenchmark !== "") filter_field["benchmark"] = [selectedBenchmark];
        if (selectedPlatform !== "") filter_field["platform"] = [selectedPlatform];
        setHostPayload({
            os_type: selectedDeviceType,
            selected_fields: ["host"],
            filter_fields: filter_field,
        });
    }, [sidebarItems, selectedBenchmark, selectedPlatform]);

    useEffect(() => {
        setIsSubHostTableEmpty(true);
        setSubHostPayload({
            os_type: selectedDeviceType,
            selected_fields: ["host"],
            filter_fields: { benchmark: [selectedBenchmark] },
        });
        setSelectedSubHost([]);
    }, [selectedBenchmark]);

    const resetSelected = (): void => {
        setMsg("");
        setSelectedBenchmark("");
        setSelectedPlatform("");
        setSidebarItems([]);
        setSelectedHost([]);
        setBenchmarkOptions({ options: [] });
        setSelectedSubHost([]);
        setHostPayload({});
        setAllSubHost([]);
        setIsSubHostTableEmpty(true);
    };

    const handleSubmit = async () => {
        if (allSubHost.length === 0) {
            setMsg("No Host No Job!");
            return;
        }
        setMsg("Sending in Job, Please wait");
        let selfQueryPayload: { [key: string]: any } = {};
        let cataglogParam: string = "";
        switch (selectedDeviceType) {
            case "Network Device":
                selfQueryPayload = {
                    os_type: selectedDeviceType,
                    selected_fields: ["host", "uuid", "cisid"],
                    filter_fields: { host: allSubHost },
                };
                cataglogParam = "payload-organizer";
                break;
            case "Linux Server":
                selfQueryPayload = {
                    os_type: selectedDeviceType,
                    selected_fields: ["host", "cisid"],
                    filter_fields: { host: allSubHost },
                };
                cataglogParam = "payload-organizer";
                break;
            case "Windows Server":
                selfQueryPayload = {
                    os_type: selectedDeviceType,
                    selected_fields: ["host", "cisid"],
                    filter_fields: { host: allSubHost },
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
        if (selectedDeviceType === "Network Device") {
            const uuidArray: Array<string> = "uuid" in data.selected_data ? data.selected_data.uuid : [];
            hostArray.forEach((value: string, index: number) => {
                payloadCiName.push({
                    hostname: value,
                    SessionID: cisidArray.length == hostArray.length && cisidArray[index] ? cisidArray[index] : "",
                    ciUUID: uuidArray.length == hostArray.length && uuidArray[index] ? uuidArray[index] : "",
                });
            });
        } else {
            hostArray.forEach((value: string, index: number) => {
                payloadCiName.push({
                    hostname: value,
                    SessionID: "",
                });
            });
        }

        let payload: { [key: string]: any } = {};
        if (selectedDeviceType === "Windows Server") {
            payload = {
                SessionID: "0",
                requestType: "cm:instance scan for " + selectedDeviceType,
                request_control_id: "ldap user upn",
                ciType: selectedDeviceType,
                ciName: payloadCiName,
                CISBenchmark: selectedBenchmark,
            };
        } else {
            payload = {
                extra_vars: {
                    SessionID: "0",
                    requestType: "cm:instance scan for " + selectedDeviceType,
                    request_control_id: "ldap user upn",
                    ciType: selectedDeviceType,
                    ciName: payloadCiName,
                    CISBenchmark: selectedBenchmark,
                },
            };
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

    const handleClickForTableBody = (obj: IHostBody, selectedArray: string[], setSelectedArray: Function) => {
        if (selectedArray.includes(obj.host)) {
            setSelectedArray(selectedArray.filter((name: string) => name !== obj.host));
        } else {
            selectedArray.push(obj.host);
            setSelectedArray([...selectedArray]);
        }
    };

    const payloadHasObject = (name: string, payload: { [key: string]: any }) => {
        return "filter_fields" in payload && payload["filter_fields"][name];
    };
    return (
        <ThemeProvider theme={theme}>
            <Stack style={{ flexDirection: "row", justifyContent: "space-between" }}>
                <Stack
                    style={{
                        width: "-webkit-fill-available",
                        alignItems: "centre",
                        marginTop: "1%",
                        marginRight: "2%",
                        borderRadius: 10,
                        paddingRight: "2%",
                        paddingBottom: "1%",
                    }}
                >
                    <h3> Compliance Ad Hoc Scanning </h3>
                    <AutocompleteButton<IButton>
                        header="Device Type"
                        value={selectedDeviceType}
                        setValue={setSelectedDeviceType}
                        list={deviceTypeOptions}
                    />

                    <AutocompleteButton<IButton>
                        header="Benchmark"
                        value={selectedBenchmark}
                        list={benchmarkOptions}
                        setValue={setSelectedBenchmark}
                    />

                    {selectedDeviceType !== "" && (
                        <Stack>
                            {((selectedBenchmark !== "" && payloadHasObject("benchmark", hostPayload)) ||
                                (selectedPlatform !== "" && payloadHasObject("platform", hostPayload))) && (
                                <Stack
                                    style={{ marginTop: "2%" }}
                                    direction={{ xs: "column", sm: "row" }}
                                    spacing={{ xs: 1, sm: 2, md: 4 }}
                                    sx={{ width: "100%", height: "100%" }}
                                    alignItems="start"
                                    justifyContent={"space-between"}
                                >
                                    <EnhancedTable<IHostHead, IHostBody>
                                        api={"/services/form/os_self_query/"}
                                        requestType="post"
                                        payload={hostPayload}
                                        columnsHead={formHostColumnHead}
                                        columnsBody={formHostColumnBody}
                                        defaultOrderBy={"host"}
                                        handleClick={handleClickForTableBody}
                                        selectedObj={selectedHost}
                                        setSelectedObj={setSelectedHost}
                                        selectedObjName="host"
                                    />
                                    <Stack
                                        direction={{ xs: "row", sm: "column" }}
                                        spacing={{ xs: 1, sm: 2, md: 4 }}
                                        alignSelf={"center"}
                                    >
                                        <Button onClick={handleMoveRight} variant="contained">
                                            <ArrowRightIcon />
                                        </Button>
                                        <Button onClick={handleMoveLeft} variant="contained">
                                            <ArrowLeftIcon />
                                        </Button>
                                    </Stack>
                                    <EnhancedTable<IHostHead, IHostBody>
                                        api={"/services/form/os_self_query/"}
                                        requestType="post"
                                        payload={subHostPayload}
                                        columnsHead={formSubHostColumnHead}
                                        columnsBody={formHostColumnBody}
                                        defaultOrderBy={"host"}
                                        handleClick={handleClickForTableBody}
                                        selectedObj={selectedSubHost}
                                        setSelectedObj={setSelectedSubHost}
                                        selectedObjName="host"
                                        isEmpty={isSubHostTableEmpty}
                                        setAllObj={setAllSubHost}
                                    />
                                </Stack>
                            )}
                        </Stack>
                    )}
                    {selectedDeviceType !== "" && (selectedPlatform !== "" || selectedBenchmark !== "") && (
                        <SubmitClearButton<IButton>
                            handleClear={() => {
                                resetSelected();
                                setSelectedDeviceType("");
                            }}
                            handleSubmit={handleSubmit}
                        />
                    )}
                    {msg !== "" && <h3>{msg}</h3>}
                </Stack>
                <Sidebar<ISidebar>
                    isOpen={selectedBenchmark !== ""}
                    direction="right"
                    parentSidebarItems={sidebarItems}
                    setParentSidebarItems={setSidebarItems}
                />
            </Stack>
        </ThemeProvider>
    );
}

const element = document.getElementById("app");

const root = ReactDOM.createRoot(element as HTMLElement);

root.render(<Form />);
