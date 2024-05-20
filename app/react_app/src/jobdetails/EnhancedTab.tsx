import React, { useEffect, useState } from "react";
import Terminal, { ColorMode } from "react-terminal-ui";
import parse from "html-react-parser";

import { IDetails, IResolveDetailsResponse, IResolveDetails } from "./DetailsUtils";
import { ITableColumn } from "../table/TableUtils";
import EnhancedTable from "../table/EnhancedTable";
import JSONPretty from "react-json-pretty";
import axios, { AxiosResponse } from "axios";
import { ProviderOutput } from "../forms/FormUtils";

var JSONPrettyMon = require("react-json-pretty/dist/monikai");
interface tabProps<T extends IDetails> {
    jobDesc: string | undefined;
    templateID: number | undefined;
    isFailResponse?: boolean;
}

interface JobDetailsColumn extends ITableColumn<IResolveDetailsResponse> {
    align?: "right";
    format?: (value: any) => string;
}

let jobDetailsColumns: JobDetailsColumn[] = [
    { id: "Number", label: "Number", width: "10%" },
    { id: "Eventnumber", label: "Event Number", width: "10%" },
    { id: "RunDateUtc", label: "Run Date UTC", width: "10%" },
    { id: "WorkflowName", label: "Workflow Name", width: "15%" },
    { id: "ActivityName", label: "Activity Name", width: "15%" },
    { id: "Result", label: "Result", width: "10%" },
];

export default function EnhancedTab<T extends IDetails>(props: tabProps<T>) {
    const { jobDesc, templateID, isFailResponse } = props;
    const [data, setData] = useState<IResolveDetails>();
    const [currProviderType, setCurrProviderType] = useState<string>();

    const hasDataObject = () => {
        return jobDesc !== undefined;
    };

    const getJobType = async () => {
        axios
            .post("/services/provider_type/", { template_id: templateID })
            .then(async (providerResponse: AxiosResponse) => {
                const providerType: ProviderOutput = providerResponse.data;
                setCurrProviderType(providerType.provider_type);
            })
            .catch(() => {
                console.log("Something went wrong with getting provider_type");
            });
    };

    useEffect(() => {
        if (templateID !== null) {
            getJobType();
        }
    }, []);

    useEffect(() => {
        if (currProviderType?.includes("resolve")) {
            let parsedObj: IResolveDetails;
            try {
                parsedObj = JSON.parse(jobDesc ? jobDesc : "");
                setData(parsedObj);
            } catch (e) {
                console.error("Invalid JSON:", e);
            }
        }
    }, [jobDesc]);

    return (
        <div>
            <div style={{ whiteSpace: "pre-line" }}>
                {currProviderType?.includes("ansible") && (
                    <Terminal colorMode={ColorMode.Dark}>
                        <div>{parse(jobDesc ? jobDesc : "")}</div>
                    </Terminal>
                )}
                {currProviderType?.includes("nautobot") && (
                    <Terminal colorMode={ColorMode.Dark}>
                        <JSONPretty
                            className="font"
                            data={parse(jobDesc ? jobDesc : "")}
                            theme={JSONPrettyMon}
                        ></JSONPretty>
                    </Terminal>
                )}
                {currProviderType?.includes("resolve") && hasDataObject() && (
                    <div className="table">
                        <br></br>
                        <EnhancedTable
                            api={""}
                            columnsHead={jobDetailsColumns}
                            columnsBody={jobDetailsColumns}
                            defaultOrderBy={"Number"}
                            handleClick={(obj: IResolveDetailsResponse) => {}}
                            data={data?.data.created}
                        />
                    </div>
                )}
                {isFailResponse && <div>Unable to Collect this Job Details</div>}
            </div>
        </div>
    );
}
