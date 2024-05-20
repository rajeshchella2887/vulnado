import React, { useEffect, useState } from "react";
import axios from "axios";

import { ThemeProvider } from "@emotion/react";
import ReactDOM from "react-dom/client";
import { theme } from "./Utils";
import DeployConfigPlanForm from "./forms/DeployConfigPlanForm";
import CreateConfigPlanForm from "./forms/CreateConfigPlanForm";
import { EnhancedTabPanel } from "./jobdetails/EnhancedTabPanel";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

export default function ConfigPlan() {
    const tabItems = ["Create Configuration Plan", "Deploy Configuration Plan"];
    const [value, setValue] = useState(0);
    const [currentTab, setCurrentTab] = useState<string>("");

    useEffect(() => {
        setCurrentTab(tabItems[value]);
    }, [value]);

    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
        setValue(newValue);
        setCurrentTab(tabItems[newValue]);
    };

    return (
        <ThemeProvider theme={theme}>
            <EnhancedTabPanel tabItems={tabItems} value={value} handleChange={handleChange} />
            <br></br>
            {currentTab.includes("Create") && <CreateConfigPlanForm />}
            {currentTab.includes("Deploy") && <DeployConfigPlanForm />}
        </ThemeProvider>
    );
}

const element = document.getElementById("app");

const root = ReactDOM.createRoot(element as HTMLElement);

root.render(<ConfigPlan />);
