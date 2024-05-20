import React, { useEffect, useState } from "react";
import axios, { AxiosResponse } from "axios";
import { AutocompleteButton, SubmitClearButton } from "../buttons/Buttons";
import { IButton, ISelectList } from "../buttons/ButtonsUtils";
import { ThemeProvider } from "@emotion/react";
import { createUniqueAndSort, theme } from "../Utils";
import dayjs from "dayjs";
import {
    CatalogDetails,
    ICatalogDetailsResponse,
    IFormDetails,
    IOSSelfQueryResponse,
    IOSTypeResponse,
    OSSelfQuery,
} from "./FormUtils";

export default function DeployConfigPlanForm<T extends IFormDetails>() {
    // options
    const [CITypeOptions, setCITypeOptions] = useState<ISelectList<IButton>>({
        options: [],
    });
    const [hostnameOptions, setHostnameOptions] = useState<ISelectList<IButton>>({
        options: [],
    });
    const [crTicketsOptions, setCRTicketsOptions] = useState<ISelectList<IButton>>({ options: [] });
    const [startTimeOptions, setStartTimeOptions] = useState<ISelectList<IButton>>({ options: [] });
    const [endTimeOptions, setEndTimeOptions] = useState<ISelectList<IButton>>({
        options: [],
    });

    const [OSType, setOSType] = useState<IOSTypeResponse<T>>();
    const [selectedCIType, setSelectedCIType] = useState<string>("");
    const [selectedDeployHost, setSelectedDeployHost] = useState<string>("");
    const [selectedCrTicket, setSelectedCrTicket] = useState<string>("");
    const [ticketStartTime, setTicketStartTime] = useState<string>("");
    const [ticketEndTime, setTicketEndTime] = useState<string>("");
    const [selectedBenchmark, setSelectedBenchmark] = useState<string>("");
    const [remediation_cisid, setRemediation_cisid] = useState<string>("");

    const [msg, setMsg] = useState<string>("");

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

    // Getting hostname
    useEffect(() => {
        setMsg("Please wait as we collect data for you");
        if (selectedCIType !== "") {
            axios
                .post("/services/form/os_self_query/", {
                    os_type: selectedCIType,
                    selected_fields: ["host"],
                    filter_fields: {},
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
                    setMsg("Something went wrong with collecting data Ticket");
                });
        }
    }, [selectedCIType]);

    // Getting CR Tickets
    useEffect(() => {
        setMsg("Please wait as we collect data for you");
        if (selectedDeployHost !== "") {
            axios
                .post("/services/form/os_self_query/", {
                    os_type: selectedCIType,
                    selected_fields: ["itsmcr", "benchmark"],
                    filter_fields: {
                        configplan: true,
                        host: [selectedDeployHost],
                    },
                })
                .then((response: AxiosResponse) => {
                    const selfQueryRes: IOSSelfQueryResponse<IFormDetails> = response.data;
                    const data: OSSelfQuery = selfQueryRes.data;
                    setCRTicketsOptions({
                        options: data.selected_data.hasOwnProperty("itsmcr") ? data.selected_data["itsmcr"] : [],
                    });
                    setSelectedBenchmark(
                        data.selected_data.hasOwnProperty("benchmark") ? data.selected_data["benchmark"][0] : "",
                    );
                    if (crTicketsOptions.options.length === null) {
                        setMsg("There are no tickets for selected hostname");
                    }
                    setMsg("");
                })
                .catch(() => {
                    setMsg("Something went wrong with collecting data from CIS Benchmark");
                });
        }
    }, [selectedDeployHost]);

    // Getting CR tickets start, end time
    useEffect(() => {
        setMsg("Please wait as we collect data for you");
        if (selectedCrTicket !== "") {
            axios
                .post("/services/form/os_self_query/", {
                    os_type: selectedCIType,
                    selected_fields: ["itsmcr_start", "itsmcr_end", "remediation_cisid"],
                    filter_fields: {
                        configplan: true,
                        itsmcr: [selectedCrTicket],
                    },
                })
                .then((response: AxiosResponse) => {
                    const selfQueryRes: IOSSelfQueryResponse<IFormDetails> = response.data;
                    const data: OSSelfQuery = selfQueryRes.data;
                    setStartTimeOptions({
                        options: createUniqueAndSort(
                            data.selected_data.hasOwnProperty("itsmcr_start") ? data.selected_data["itsmcr_start"] : [],
                        ),
                    });
                    setEndTimeOptions({
                        options: createUniqueAndSort(
                            data.selected_data.hasOwnProperty("itsmcr_end") ? data.selected_data["itsmcr_end"] : [],
                        ),
                    });
                    setRemediation_cisid(
                        data.selected_data.hasOwnProperty("remediation_cisid")
                            ? data.selected_data["remediation_cisid"][0]
                            : "",
                    );

                    if (startTimeOptions.options.length > 0) {
                        setTicketStartTime(startTimeOptions.options[0]);
                    } else {
                        setTicketStartTime("");
                    }

                    if (endTimeOptions.options.length > 0) {
                        setTicketEndTime(endTimeOptions.options[0]);
                    } else {
                        setTicketEndTime("");
                    }

                    setMsg("");
                })
                .catch(() => {
                    setMsg("Something went wrong with collecting data from CIS Benchmark");
                });
        }
    }, [selectedCrTicket]);

    const generateSQPayloadAndCatalog = (selectedCIType: string) => {
        let selfQueryPayload: { [key: string]: any } = {};
        let cataglogParam: string = "";

        switch (selectedCIType) {
            case "Network Device":
                selfQueryPayload = {
                    os_type: selectedCIType,
                    selected_fields: ["host", "uuid", "remediation_cisid"],
                    filter_fields: { host: [selectedDeployHost] },
                };
                cataglogParam = "Resolve Launch job";
                break;
            case "Linux Server":
                selfQueryPayload = {
                    os_type: selectedCIType,
                    selected_fields: ["host", "remediation_cisid"],
                    filter_fields: { host: [selectedDeployHost] },
                };
                cataglogParam = "payload-organizer";
                break;
            case "Windows Server":
                selfQueryPayload = {
                    os_type: selectedCIType,
                    selected_fields: ["host", "remediation_cisid"],
                    filter_fields: { host: [selectedDeployHost] },
                };
                cataglogParam = "Resolve Launch job";
                break;
        }
        return { selfQueryPayload, cataglogParam };
    };

    const getSQAndCatalogData = async (SQpayload: { [keys: string]: any }, cataglogParam: string) => {
        let selfQueryResponse: { [keys: string]: any } = {};
        await axios
            .post("/services/form/os_self_query/", SQpayload)
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
        return { data, catalogData };
    };

    const generateLaunchJobPayload = async (data: OSSelfQuery) => {
        const hostArray: Array<string> = "host" in data.selected_data ? (data.selected_data.host as string[]) : [];
        const payloadCiName: { [key: string]: string }[] = [];
        if (selectedCIType === "Network Device") {
            const uuidArray: Array<string> = "uuid" in data.selected_data ? data.selected_data.uuid : [];
            let configplanUUID = "";
            await axios
                .post("/services/form/os_self_query/", {
                    os_type: "Network Device",
                    selected_fields: ["cm_configplan_uuid"],
                    filter_fields: { host: [selectedDeployHost] },
                })
                .then((response: AxiosResponse) => {
                    configplanUUID = response.data.data["selected_data"]["cm_configplan_uuid"][0];
                })
                .catch(() => {
                    setMsg("Something went wrong with collecting cm_configplanUUID");
                });
            hostArray.forEach((value: string, index: number) => {
                payloadCiName.push({
                    hostname: value,
                    hostUUID: uuidArray.length == hostArray.length && uuidArray[index] ? uuidArray[index] : "",
                    configplanUUID: configplanUUID,
                });
            });
        } else {
            payloadCiName.push({
                hostname: selectedDeployHost,
                SessionID: remediation_cisid,
            });
        }

        let payload: { [key: string]: any } = {};
        if (selectedCIType === "Linux Server") {
            payload = {
                extra_vars: {
                    SessionID: "0",
                    requestType: "cm:configplan deployment for " + selectedCIType,
                    request_control_id: "idap user upn",
                    ciType: selectedCIType,
                    ciName: payloadCiName,
                    configPlanITSMCR: selectedCrTicket,
                    CISBenchmark: selectedBenchmark,
                },
            };
        } else if (selectedCIType === "Network Device") {
            payload = {
                SessionID: "0",
                requestType: "cm:configplan deployment for " + selectedCIType,
                request_control_id: "idap user upn",
                ciType: selectedCIType,
                ciName: payloadCiName,
                configPlanITSMCR: selectedCrTicket,
                // CISBenchmark: selectedBenchmark,
            };
        } else if (selectedCIType === "Windows Server") {
            // for windows & network
            payload = {
                SessionID: "0",
                requestType: "cm:configplan deployment for " + selectedCIType,
                request_control_id: "idap user upn",
                ciType: selectedCIType,
                ciName: payloadCiName,
                configPlanITSMCR: selectedCrTicket,
                CISBenchmark: selectedBenchmark,
            };
        }
        return payload;
    };

    const handleSubmit = async () => {
        if (selectedCrTicket === "") {
            setMsg("No Ticket No Job");
            return;
        }
        const currentDateTime = dayjs().format("YYYY-MM-DD HH:mm:ss");
        const newticketStartTime = dayjs(ticketStartTime, "YYYY-MM-DD HH:mm:ss");
        const newticketEndTime = dayjs(ticketEndTime, "YYYY-MM-DD HH:mm:ss");

        // check if the current time fits in the CR start and end time
        if (newticketStartTime.isAfter(currentDateTime) || newticketEndTime.isBefore(currentDateTime)) {
            setMsg(
                "Unable to send form. Sending of form must be within the time frame set in the creation of config plan form.",
            );
            return;
        }

        setMsg("Sending in Job, Please wait");
        const { selfQueryPayload, cataglogParam } = generateSQPayloadAndCatalog(selectedCIType);

        const { data, catalogData } = await getSQAndCatalogData(selfQueryPayload, cataglogParam);

        const payload = await generateLaunchJobPayload(data);

        if (selectedCIType === "Network Device") {
            let deploy_configplan_uuid = "";
            await axios
                .post("/services/form/os_self_query/", {
                    os_type: "Network Device",
                    selected_fields: ["sp_configplan_name", "sp_configplan_uuid"],
                    filter_fields: {
                        configplan_name: "Deploy Config Plan",
                    },
                })
                .then((response: AxiosResponse) => {
                    deploy_configplan_uuid = response.data.data["selected_data"]["sp_configplan_uuid"][0];
                })
                .catch(() => {
                    setMsg("Something went wrong with collecting deploy configplan_uuid");
                    return;
                });
            let objectModel = "";
            await axios
                .post("/services/form/os_self_query/", {
                    os_type: "Network Device",
                    selected_fields: ["configplan_objectmodel"],
                    filter_fields: {},
                })
                .then((response: AxiosResponse) => {
                    objectModel = response.data.data["selected_data"]["configplan_objectmodel"][0];
                })
                .catch(() => {
                    setMsg("Something went wrong with collecting configplan_objectmodel");
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
            payload["deploy_configplan_uuid"] = deploy_configplan_uuid;
            payload["nbcr_approved_uuid"] = nbcrUUID;
            payload["configplan_objectmodel"] = objectModel;
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
        setSelectedDeployHost("");
        setSelectedCrTicket("");
    };

    return (
        <ThemeProvider theme={theme}>
            <h3>Deploy Config Plan</h3>
            <AutocompleteButton<IButton>
                header="CI Type"
                value={selectedCIType}
                setValue={setSelectedCIType}
                list={CITypeOptions}
            />
            <br></br>
            <AutocompleteButton<IButton>
                header="Hostname"
                value={selectedDeployHost}
                setValue={setSelectedDeployHost}
                list={hostnameOptions}
            />
            <br></br>
            {selectedDeployHost !== "" && (
                <AutocompleteButton<IButton>
                    header="CR Ticket"
                    value={selectedCrTicket}
                    setValue={setSelectedCrTicket}
                    list={crTicketsOptions}
                />
            )}

            {msg !== "" && <h5>{msg}</h5>}

            <SubmitClearButton<IButton> handleClear={resetSelected} handleSubmit={handleSubmit} />
        </ThemeProvider>
    );
}
