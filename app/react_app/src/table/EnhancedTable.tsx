import React from "react";
import { useState, useEffect } from "react";
import axios, { Axios, AxiosError, AxiosResponse } from "axios";

import { Checkbox, ThemeProvider } from "@mui/material";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableContainer from "@mui/material/TableContainer";
import TablePagination from "@mui/material/TablePagination";

import { ITableRow, ITableColumn, Order, ITableResponse } from "./TableUtils";
import EnhancedTableHead from "./EnhancedTableHead";
import EnhancedTableBody from "./EnhancedTableBody";
import SearchBar from "./SearchBar";

import { colors, theme } from "../Utils";
import "./EnhancedTable.css";
import {
    AnsibleStatusOutput,
    IAnsibleStatusOutputResponse,
    IFormDetails,
    IOSSelfQueryResponse,
    IProviderOutputResponse,
    OSSelfQuery,
    ProviderOutput,
} from "../forms/FormUtils";

interface props<TableHead extends ITableRow, TableBody extends ITableRow> {
    api: string;
    requestType?: "get" | "post";
    payload?: Object;
    columnsHead: Array<ITableColumn<TableHead>>;
    columnsBody: Array<ITableColumn<TableBody>>;
    defaultOrderBy: keyof TableHead;
    handleClick: Function;
    selectedObj?: Array<string>;
    setSelectedObj?: (array: Array<string>) => void;
    selectedObjName?: string;
    isEmpty?: boolean;
    setAllObj?: Function;
    data?: Array<TableBody>;
    isPolling?: boolean;
}

export default function EnhancedTable<TableHead extends ITableRow, TableBody extends ITableRow>(
    props: props<TableHead, TableBody>,
) {
    const [bodyNameArray, setBodyNameArray] = useState<Array<string>>([]);
    const [resultArray, setResultArray] = useState<Array<{ [key: string]: any }>>([]);
    const [response, setResponse] = useState<ITableResponse<TableBody>>();
    const [data, setData] = useState<TableBody[]>([]);
    const [order, setOrder] = useState<Order>("desc");
    const [orderBy, setOrderBy] = useState<keyof TableHead>(props.defaultOrderBy);
    const [page, setPage] = useState<number>(0);
    const [rowsPerPage, setRowsPerPage] = useState<number>(5);
    const [searchFilter, setSearchFilter] = useState<string>("");

    const [deployTimer, setDeployTimer] = useState<number>(0);
    const [resetTime, setResetTime] = useState<number>(10);
    const [pollingItem, setPollingItem] = useState<Array<TableBody>>([]);
    const [isSearchLocally, setIsSearchLocally] = useState<boolean>(false);

    useEffect(() => {
        if (props.isPolling) {
            setDeployTimer(resetTime);
        }
    }, []);

    useEffect(() => {
        if (deployTimer > 0) {
            setTimeout(() => setDeployTimer(deployTimer - 1), 1000);
        } else {
            // do the check
            if (pollingItem.length) {
                const newPollingItem: TableBody[] = [];
                pollingItem.forEach(async (item: TableBody) => {
                    // call getProviderView from automation
                    // call  jobstatus from automation
                    const templateID = "template" in item ? item["template"] : 0;
                    await axios
                        .post("/services/provider_type/", { template_id: templateID })
                        .then(async (providerResponse: AxiosResponse) => {
                            const providerType: ProviderOutput = providerResponse.data;
                            if (providerType.provider_type === "ansible") {
                                let status_url: string = "stdout_api" in item ? (item["stdout_api"] as string) : "";
                                status_url = status_url.replace("stdout/", "");
                                const job_id = "job_id" in item ? item["job_id"] : 0;
                                await axios
                                    .get("/services/ajax/launchjob/status/", {
                                        params: {
                                            status_url: status_url,
                                            template_id: templateID,
                                            job_id: job_id,
                                        },
                                    })
                                    .then((statusResponese: AxiosResponse) => {
                                        const statusData: AnsibleStatusOutput = statusResponese.data;

                                        if (
                                            statusData.status.toLowerCase() !== "successful" ||
                                            statusData.status.toLowerCase() !== "failed" ||
                                            statusData.status.toLowerCase() !== "canceled"
                                        ) {
                                            newPollingItem.push(item);
                                            setDeployTimer(resetTime);
                                        }
                                    })
                                    .catch(() => {
                                        console.log("Something went wrong with status collection");
                                    });
                            }
                        })
                        .catch(() => {
                            console.log("Something went wrong with getting provider_type");
                        });
                });
                setPollingItem(newPollingItem); // may cause the it to continusely remove
                getTableResponse();
            } else {
                setDeployTimer(resetTime);
            }
        }
    }, [deployTimer]);

    const getTableResponse = async () => {
        let tableResponse: ITableResponse<TableBody> = {
            data: {
                count: resultArray.length,
                next: "",
                previous: "",
                results: [],
                current_page: page + 1,
                per_page: rowsPerPage,
                total_pages: Math.ceil(resultArray.length / rowsPerPage),
                page_range: [],
            },
            success: true,
        };
        setResponse(tableResponse);
        setData([]);
        if (!props.isEmpty) {
            if (props.api !== "") {
                if (props?.requestType && props.requestType === "post") {
                    // making a deep copy of payload
                    let payload: { [key: string]: { [key: string]: any } } = props.payload
                        ? JSON.parse(JSON.stringify(props.payload))
                        : {};
                    if (!isSearchLocally) payload["filter_fields"]["search"] = searchFilter;

                    const selectedName = props.selectedObjName ? props.selectedObjName : "";
                    axios
                        .post(props.api, payload)
                        .then((response: AxiosResponse) => {
                            const selfQueryRes: IOSSelfQueryResponse<IFormDetails> = response.data;
                            const data: OSSelfQuery = selfQueryRes.data;
                            const selectedArray: string[] = data.selected_data.hasOwnProperty(selectedName)
                                ? data.selected_data[selectedName]
                                : [];
                            let resultArray: Object[] = [];
                            const finalSelected: string[] = [];
                            selectedArray.forEach((selected: string) => {
                                if (selected.includes(",")) {
                                    setIsSearchLocally(true);
                                    const newArray = selected.split(",");
                                    newArray.forEach((curr: string) => {
                                        resultArray.push({ [selectedName]: curr });
                                        finalSelected.push(curr);
                                    });
                                } else {
                                    resultArray.push({ [selectedName]: selected });
                                    finalSelected.push(selected);
                                }
                            });
                            if (searchFilter !== "")
                                resultArray = resultArray.filter((item) =>
                                    hasStringContainingFilter(item, searchFilter),
                                );
                            resultArray.sort();
                            setResultArray(resultArray);
                            const tableResponse = {
                                data: {
                                    count: resultArray.length,
                                    next: "",
                                    previous: "",
                                    results: resultArray.slice(
                                        page * rowsPerPage,
                                        Math.min(page * rowsPerPage + rowsPerPage, resultArray.length),
                                    ) as TableBody[],
                                    current_page: page + 1,
                                    per_page: rowsPerPage,
                                    total_pages: Math.ceil(resultArray.length / rowsPerPage),
                                    page_range: [],
                                },
                                success: true,
                            };
                            setResponse(tableResponse);
                            finalSelected.sort();
                            setBodyNameArray(finalSelected);
                            if (props.setAllObj) props.setAllObj(selectedArray);
                        })
                        .catch((error: AxiosError) => {
                            console.log(error);
                        });
                } else {
                    axios
                        .get(props.api, {
                            params: {
                                page: page + 1,
                                page_size: rowsPerPage,
                                search: searchFilter,
                                ordering: orderBy.toString(),
                                order: order.toString(),
                            },
                        })
                        .then(function (response: AxiosResponse) {
                            setResponse(response.data);
                            setData(response.data.data);
                        })
                        .catch(function (error) {
                            console.log(error);
                        });
                }
            } else {
                setData(props.data ? props.data : []);
            }
        }
    };

    const hasStringContainingFilter = (data: any, filter: string): boolean => {
        if (typeof data === "string") {
            return data.includes(filter); // Optimized string search
        } else if (Array.isArray(data)) {
            return data.some((item) => hasStringContainingFilter(item, filter)); // Check for "abc" in any element
        } else if (typeof data === "object") {
            for (const key in data) {
                if (hasStringContainingFilter(data[key], filter)) return true;
            }
            return false;
        } else {
            return false; // Non-strings and non-arrays are not considered
        }
    };

    useEffect(() => {
        getTableResponse();
    }, [page, rowsPerPage, orderBy, order, searchFilter, props.api, props.payload, props.isEmpty]);

    useEffect(() => {
        if (props.data) {
            setResultArray([]);
            setData(props.data);
        }
    }, [props.data]);

    useEffect(() => {
        // get jobs to work on
        if (props.isPolling) {
            const curPollingItem: Array<TableBody> = [];
            response?.data.results.forEach((item: TableBody) => {
                if ("status" in item) {
                    const status: string = (item["status"] as string).toLowerCase();
                    if (status !== "successful" && status !== "failed" && status !== "canceled") {
                        curPollingItem.push(item);
                    }
                }
            });
            setPollingItem(curPollingItem);
        }
    }, [response]);

    function handleRequestSort(e: React.MouseEvent<unknown>, property: keyof TableHead) {
        const isAsc = orderBy === property && order === "desc";
        setOrder(isAsc ? "asc" : "desc");
        setOrderBy(property);
        setPage(0);
    }

    function handlePageChange(e: unknown, newPage: number) {
        setPage(newPage);
    }

    function handleChangeRowsPerPage(e: React.ChangeEvent<HTMLInputElement>) {
        setRowsPerPage(+e.target.value);
        setPage(0);
    }

    function handleChangeSearchFilter(search: string) {
        setSearchFilter(search);
        setPage(0);
    }
    return (
        <ThemeProvider theme={theme}>
            <Paper sx={{ width: "100%", overflow: "hidden" }}>
                <SearchBar handleChange={(e: string) => handleChangeSearchFilter(e)} />
                <TableContainer sx={{ width: "inherit" }}>
                    {props.columnsHead.length !== props.columnsBody.length ? (
                        <Table stickyHeader aria-label="table" sx={{ color: "white", width: "inherit" }}>
                            <EnhancedTableHead
                                columns={props.columnsHead}
                                order={order}
                                orderBy={orderBy}
                                onRequestSort={handleRequestSort}
                                selectedObj={props.selectedObj}
                                setSelectedObj={props.setSelectedObj}
                                allObj={bodyNameArray}
                            />
                        </Table>
                    ) : (
                        <Table stickyHeader aria-label="table" sx={{ color: "white", width: "inherit" }}>
                            <EnhancedTableHead
                                columns={props.columnsHead}
                                order={order}
                                orderBy={orderBy}
                                onRequestSort={handleRequestSort}
                                selectedObj={props.selectedObj}
                                setSelectedObj={props.setSelectedObj}
                                allObj={bodyNameArray}
                            />
                            <EnhancedTableBody
                                rowData={props.data ? data : response ? response.data.results : []}
                                columns={props.columnsBody}
                                handleClick={props.handleClick}
                                selectedObj={props.selectedObj}
                                setSelectedObj={props.setSelectedObj}
                                selectedObjName={props.selectedObjName}
                            />
                        </Table>
                    )}
                    {props.columnsHead.length !== props.columnsBody.length ? (
                        <Table stickyHeader aria-label="table" sx={{ color: "white", width: "inherit" }}>
                            <EnhancedTableBody
                                rowData={props.data ? data : response ? response.data.results : []}
                                columns={props.columnsBody}
                                handleClick={props.handleClick}
                                selectedObj={props.selectedObj}
                                setSelectedObj={props.setSelectedObj}
                                selectedObjName={props.selectedObjName}
                            />
                        </Table>
                    ) : (
                        <></>
                    )}
                </TableContainer>
                <TablePagination
                    rowsPerPageOptions={[5, 10, 25, 100]}
                    component="div"
                    count={props.data ? 0 : response ? response.data.count : 0}
                    rowsPerPage={rowsPerPage}
                    page={page}
                    onPageChange={handlePageChange}
                    onRowsPerPageChange={handleChangeRowsPerPage}
                    sx={{ backgroundColor: colors.tertiary, color: "white" }}
                />
            </Paper>
        </ThemeProvider>
    );
}
