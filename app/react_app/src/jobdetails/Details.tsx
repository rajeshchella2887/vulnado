import React, { useEffect, useState } from "react";
import { IDetails, IDetailsResponse } from "./DetailsUtils";
import axios, { AxiosResponse } from "axios";
import { ThemeProvider } from "@emotion/react";
import { theme } from "../Utils";
import EnhancedTab from "./EnhancedTab";

interface props<T extends IDetails> {
    api: string;
    jobUUID: string | undefined;
    templateID?: number | undefined;
}

export default function Details<T extends IDetails>(props: props<T>) {
    const [response, setResponse] = useState<IDetailsResponse<T>>();
    const [isFailResponse, setIsFailResponse] = useState<boolean>(false);
    useEffect(() => {
        axios
            .get(props.api, {
                params: {
                    job_uuid: props.jobUUID,
                    template_id: props.templateID,
                },
            })
            .then(function (response: AxiosResponse) {
                setResponse(response.data);
            })
            .catch(function (error) {
                setIsFailResponse(true);
                console.log(error);
            });
    }, []);

    return (
        <ThemeProvider theme={theme}>
            <div>
                <h3>Job UUID: {props.jobUUID}</h3>
                <EnhancedTab jobDesc={response?.data} templateID={props.templateID} isFailResponse={isFailResponse} />
            </div>
        </ThemeProvider>
    );
}
