import React, { useState, useEffect } from "react";
import { DateTimeValidationError, PickerChangeHandlerContext } from "@mui/x-date-pickers";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import Alert from "@mui/material/Alert";

interface props {
    label: string;
    value: any;
    onChange: ((value: any, context: PickerChangeHandlerContext<DateTimeValidationError>) => void) | undefined;
}

export default function DatePickerButton(props: Readonly<props>) {
    const [cleared, setCleared] = useState<boolean>(false);

    useEffect(() => {
        if (cleared) {
            const timeout = setTimeout(() => {
                setCleared(false);
            }, 1500);

            return () => clearTimeout(timeout);
        }
        return () => {};
    }, [cleared]);

    return (
        <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DateTimePicker
                label={props.label}
                sx={{ width: 260 }}
                slotProps={{
                    field: { clearable: true, onClear: () => setCleared(true) },
                }}
                value={props.value}
                onChange={props.onChange}
            />

            {cleared && (
                <Alert sx={{ position: "absolute", bottom: 0, right: 0 }} severity="success">
                    Field cleared!
                </Alert>
            )}
        </LocalizationProvider>
    );
}
