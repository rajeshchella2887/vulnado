import React from "react";
import { createTheme } from "@mui/material";

export const colors = {
    primary: "#3B4650", //greyPrimary
    secondary: "#4B5966", //greySecondary
    tertiary: "#39434D", //greyPrimaryHeader
    hover: "#0071BC", //bgBlue
};

export const theme = createTheme({
    typography: {
        fontFamily: [
            "Poppins",
            "Roboto",
            "Open Sans",
            "Segoe UI",
            "Oxygen",
            "Ubuntu",
            "Cantarell",
            "Fira Sans",
            "Droid Sans",
            "Helvetica Neue",
            "sans-serif",
        ].join(","),
        fontSize: 14,
    },
});

export const createUniqueAndSort = (value: string[]) => {
    const uniques: string[] = value.filter((value: string, index: number, self) => {
        return self.indexOf(value) === index;
    });
    uniques.sort();
    return uniques;
};
