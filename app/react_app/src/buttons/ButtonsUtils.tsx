import React from "react";

export interface IButton {}

export interface ISelectList<T extends IButton> {
    options: Array<string>;
}

export interface buttonProps<T extends IButton> {
    header: string;
    value: string | null;
    list: ISelectList<T>;
    setValue?: Function;
}

export interface submitClearProps<T extends IButton> {
    handleClear: Function;
    handleSubmit: Function;
}
