import React from "react";
import { ITableRow } from "../table/TableUtils";

export interface IDetails {}

export interface IDetailsResponse<T extends IDetails> {
    data: string;
    success: boolean;
}

export interface IResolveDetailsResponse extends ITableRow {
    Number: string;
    Eventnumber: string;
    RunDate: string;
    RunDateUtc: string;
    Eventtype: string;
    Subject: string;
    Message: string;
    Status: string;
    StatusColor: string;
    WorkflowName: string;
    BranchName: string;
    ActivityName: string;
    FullName: string;
    DutyName: string;
    Module: string;
    GroupName: string;
    Result: string;
    ResultType: string;
    ModifiedDate: string;
    LastModify: string;
    LastCreate: string;
    Remark: string;
    BodyLength: Number;
    Trigger: string;
    EventParser: string;
}

export interface IResolveData {
    created: IResolveDetailsResponse[];
}

export interface IResolveDetails {
    innerCode: Number;
    data: IResolveData;
}
