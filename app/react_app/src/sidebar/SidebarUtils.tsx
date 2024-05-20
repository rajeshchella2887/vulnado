import { SvgIconTypeMap } from "@mui/material";
import { OverridableComponent } from "@mui/material/OverridableComponent";

export interface ISidebar {}

export interface SidebarItem<T extends ISidebar> {
    name: string;
    icon?: OverridableComponent<SvgIconTypeMap<{}, "svg">> & {
        muiName: string;
    };
    children?: SidebarItem<T>[];
    selected?: Boolean;
}

export interface MenuProps<T extends ISidebar> {
    item: SidebarItem<T>;
    isChild: boolean;
    lv: number;
    setParentSidebarItems?: Function;
    parentSidebarItems?: SidebarItem<T>[];
}

export interface SidebarProps<T extends ISidebar> {
    isOpen: boolean;
    direction: "left" | "right";
    parentSidebarItems: SidebarItem<T>[];
    setParentSidebarItems?: Function;
}
