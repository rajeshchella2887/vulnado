import React, { useState } from "react";

// MUI imports
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Box from "@mui/material/Box";

// File Imports
import TabPanel from "./TabPanel";

interface props {
    tabItems: Array<string>;
    value: number;
    uuid?: string;
    handleChange?: (event: React.SyntheticEvent, newValue: number) => void;
}

function a11yProps(index: number) {
    return {
        id: `simple-tab-${index}`,
        "aria-controls": `simple-tabpanel-${index}`,
    };
}

export function EnhancedTabPanel(props: props) {
    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        props.value = newValue;
    };
    return (
        <Box sx={{ width: "100%" }}>
            <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
                <Tabs value={props.value} onChange={props.handleChange} aria-label="job desc tabs" textColor="inherit">
                    {props.tabItems.map((string, index) => (
                        <Tab label={string} {...a11yProps(index)} key={index} />
                    ))}
                </Tabs>
            </Box>
        </Box>
    );
}
