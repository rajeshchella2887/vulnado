import React from "react";
import ReactDOM from "react-dom/client";

import Details from "./jobdetails/Details";
import axios from "axios";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
interface IJob {
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

export function JobDetails() {
    // Retrieve the data from localStorage
    const storedData = localStorage.getItem("selectedRow");
    let selectedRow: IJob | null = null;

    if (storedData !== null) {
        selectedRow = JSON.parse(storedData);
    } else {
        console.log("No data stored for selectedRow");
    }

    localStorage.removeItem("selectedRow");

    return selectedRow ? (
        <Details
            api={"/services/job-details/"}
            jobUUID={selectedRow?.job_uuid?.toString()}
            templateID={Number(selectedRow?.template)}
        />
    ) : null;
}

const element = document.getElementById("details");

const root = ReactDOM.createRoot(element as HTMLElement);

root.render(<JobDetails />);
