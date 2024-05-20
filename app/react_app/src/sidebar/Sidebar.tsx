import React from "react";

import { Drawer } from "@mui/material";
import { styled } from "@mui/material/styles";

// Icons input
import List from "@mui/material/List";

import MenuItem from "./MenuItem";
import { ISidebar, SidebarProps } from "./SidebarUtils";
import { colors } from "../Utils";

import "./Sidebar.css";

export default function Sidebar<T extends ISidebar>(props: SidebarProps<T>) {
    //Header
    const appBarHeight = 0;
    //Sidebar
    const drawerWidth = 280;

    const DrawerHeader = styled("div")(({ theme }) => ({
        display: "flex",
        alignItems: "center",
        padding: theme.spacing(0, 1),
        justifyContent: "flex-end",
        height: appBarHeight,
    }));

    const items = props.parentSidebarItems;
    return (
        <Drawer
            variant="persistent"
            anchor={props.direction}
            className="sidebarDrawer"
            PaperProps={{
                sx: {
                    width: drawerWidth,
                    backgroundColor: colors.primary,
                    color: "white",
                    position: "sticky",
                },
            }}
            open={props.isOpen}
        >
            <DrawerHeader />
            <List className="sidebarList" sx={{ overflow: "hidden" }}>
                {items.map((sidebarItem, key) => (
                    <MenuItem
                        item={sidebarItem}
                        isChild={false}
                        lv={0}
                        key={key}
                        setParentSidebarItems={props.setParentSidebarItems}
                        parentSidebarItems={props.parentSidebarItems}
                    />
                ))}
            </List>
        </Drawer>
    );
}
