import React, { ReactNode, useState } from "react";
import {
    Autocomplete,
    AutocompleteChangeDetails,
    AutocompleteChangeReason,
    FormControl,
    MenuItem,
    Select,
    SelectChangeEvent,
    Stack,
    TextField,
    Button,
} from "@mui/material";
import { IButton, buttonProps, submitClearProps } from "./ButtonsUtils";

// Single Selected with drop down to choose from in the list
export function DropdownButton<T extends IButton>(props: Readonly<buttonProps<T>>) {
    const { header, list, value, setValue } = props;
    const [localValue, setLocalValue] = useState<string>("");

    const localHandleChange = (event: SelectChangeEvent<string>, child: ReactNode) => {
        const newValue = event.target.value;
        setLocalValue(newValue);
        if (setValue !== undefined) setValue(newValue);
    };

    return (
        <Stack style={{ flexDirection: "column" }}>
            <h4>{header}</h4>
            <FormControl className={header} sx={{ width: "48%", borderRadius: 1.5 }} size="small">
                <Select
                    labelId={header}
                    id={header + "Input"}
                    sx={{ color: "black" }}
                    value={setValue !== undefined ? (value ? value : "") : localValue}
                    onChange={localHandleChange}
                >
                    {list?.options.map((OS, key) => (
                        <MenuItem key={key} value={OS}>
                            {OS}
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        </Stack>
    );
}

// single selected with drop down and search to search from in the list
export function AutocompleteButton<T extends IButton>(props: buttonProps<T>) {
    const { header, list, value, setValue } = props;
    const [localValue, setLocalValue] = useState<string>("");

    const localHandleChange = (
        event: React.SyntheticEvent<Element, Event>,
        value: string | null,
        reason: AutocompleteChangeReason,
        details?: AutocompleteChangeDetails<string> | undefined,
    ) => {
        if (typeof value === "string") {
            const newValue = value.slice(0);
            setLocalValue(value);
            if (setValue) setValue(newValue);
        } else {
            setLocalValue("");
            if (setValue) setValue("");
        }
    };

    return (
        <Stack sx={{ width: "48%" }}>
            <h4>{header}</h4>
            <Autocomplete
                id={header + "Input"}
                options={list?.options}
                onChange={localHandleChange}
                value={setValue !== undefined ? (value ? value : null) : localValue === "" ? null : localValue}
                renderInput={(params) => (
                    <TextField
                        {...params}
                        variant="standard"
                        placeholder={header}
                        sx={{
                            input: {
                                color: "black",
                            },
                        }}
                    />
                )}
            />
        </Stack>
    );
}

export function SubmitClearButton<T extends IButton>(props: submitClearProps<T>) {
    const { handleClear, handleSubmit } = props;
    return (
        <Stack direction="row" spacing="1%" sx={{ justifyContent: "start", paddingTop: "2%" }}>
            <div className="clearButton">
                <Button
                    type="reset"
                    className="reset"
                    variant="contained"
                    onClick={() => {
                        handleClear();
                    }}
                >
                    Clear
                </Button>
            </div>
            <div className="submitButton">
                <Button
                    type="submit"
                    className="submit"
                    variant="contained"
                    onClick={() => {
                        handleSubmit();
                    }}
                >
                    Submit
                </Button>
            </div>
        </Stack>
    );
}
