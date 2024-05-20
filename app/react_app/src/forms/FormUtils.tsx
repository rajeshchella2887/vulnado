import React from "react";
import { ITableRow } from "../table/TableUtils";

export interface IFormDetails {}

export interface OSType {
    os_data: Array<string>;
}

export interface IOSTypeResponse<T extends IFormDetails> {
    data: OSType;
    success: boolean;
}

export interface OSFilter {
    region: Array<string>;
    country: Array<string>;
    site: Array<string>;
    benchmark: Array<Array<string>>;
    host: Array<string>;
    platform: Array<string>;
    uuid: Array<string>;
    cisid: Array<string>;
    itsmcr: Array<string>;
    itsmcr_start: string;
    itsmcr_end: string;
    feature: Array<string>;
}

export interface IOSFilterResponse<T extends IFormDetails> {
    data: OSFilter;
    success: boolean;
}

export interface OSQuery {
    region: Array<string>;
    country: Array<string>;
    site: Array<string>;
    host: Array<string>;
    platform: Array<string>;
}

export interface IOSQueryResponse<T extends IFormDetails> {
    data: OSQuery;
    success: boolean;
}

export interface OSSelfQuery {
    selected_data: { [key: string]: string[] };
}

export interface IOSSelfQueryResponse<T extends IFormDetails> {
    data: OSSelfQuery;
    success: boolean;
}

export interface FeatureName {
    feature_name: Array<string>;
}
export interface IFeatureNameResponse<T extends IFormDetails> {
    data: FeatureName;
    success: boolean;
}

export interface CRTickets {
    cr_tickets: Array<string>;
}

export interface ICRTicketsResponse<T extends IFormDetails> {
    data: CRTickets;
    success: boolean;
}

export interface CatalogDetails {
    catalog_template_id: number;
    catalog_launch_url: string;
}

export interface ICatalogDetailsResponse<T extends IFormDetails> {
    data: CatalogDetails;
    success: boolean;
}

export interface LaunchJobOutput {
    name: string;
    template_id: number;
    job_id: number;
    status: string;
    status_url: string;
    stdout_url: string;
    traceback_result: string;
}

export interface ILaunchJobOutputResponse<T extends IFormDetails> {
    data: LaunchJobOutput;
    success: boolean;
}

export interface ProviderOutput {
    provider_type: string;
}

export interface IProviderOutputResponse<T extends IFormDetails> {
    data: ProviderOutput;
    success: boolean;
}

export interface AnsibleStatusOutput {
    status: string;
}

export interface IAnsibleStatusOutputResponse<T extends IFormDetails> {
    data: AnsibleStatusOutput;
    success: boolean;
}

export interface ICIName {
    hostname: string;
    SessionID: string;
    feature?: string;
    ciUUID?: string;
}
