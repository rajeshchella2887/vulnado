import React from "react";
import ReactDOM from "react-dom/client";
import axios from "axios";
import { ITableRow, ITableColumn } from "./table/TableUtils";

import EnhancedTable from "./table/EnhancedTable";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
interface IJob extends ITableRow {
    job_id: number;
    name: string;
    created_dt: string;
    modified_dt: string;
    started_at: string;
    finished_at: string;
    status: string;
    template: number;
    job_uuid: string;
    stdout_api: string;
    job_type: string;
    is_sub_job: boolean;
    parent_job: string;
    order: number;
    handleClick: (e: React.MouseEvent<HTMLElement>) => void;
}

interface JobHistoryColumn extends ITableColumn<IJob> {
    align?: "right";
    format?: (value: any) => string;
}

let jobHistoryColumns: JobHistoryColumn[] = [
    { id: "job_id", label: "Job ID", width: "10%" },
    { id: "name", label: "Name", width: "10%" },
    { id: "status", label: "Status", width: "10%" },
    { id: "started_at", label: "Start Time", width: "15%" },
    { id: "finished_at", label: "Complete Time", width: "15%" },
    { id: "job_uuid", label: "Job UUID", width: "10%" },
];

export default function JobHistory() {
    return (
        <EnhancedTable<IJob, IJob>
            api={"/services/jobs-list"}
            columnsHead={jobHistoryColumns}
            columnsBody={jobHistoryColumns}
            defaultOrderBy={"job_id"}
            handleClick={(obj: IJob) => {
                localStorage.setItem("selectedRow", JSON.stringify(obj));
                window.open("/services/jobdetails/", "_self");
            }}
            isPolling={true}
        />
    );
}

const element = document.getElementById("app");

const root = ReactDOM.createRoot(element as HTMLElement);

root.render(<JobHistory />);
