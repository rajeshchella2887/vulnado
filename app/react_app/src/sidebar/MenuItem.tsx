import React, { useState, useEffect } from "react";
import { ThemeProvider } from "@mui/material";
import Collapse from "@mui/material/Collapse";
import List from "@mui/material/List";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import ExpandLessRoundedIcon from "@mui/icons-material/ExpandLessRounded";
import ExpandMoreRoundedIcon from "@mui/icons-material/ExpandMoreRounded";

import { ISidebar, MenuProps, SidebarItem } from "./SidebarUtils";
import { colors, theme } from "../Utils";

import "./Sidebar.css";

export default function MenuItem(props: MenuProps<ISidebar>) {
    function hasChildren(item: SidebarItem<ISidebar>) {
        if (item.children === undefined || item.children.length === 0) {
            return false;
        }
        return true;
    }

    const SingleLevel = (item: SidebarItem<ISidebar>) => {
        const [isSelected, setIsSelected] = useState<Boolean>(false);

        useEffect(() => {
            // getting the data to se
            if (item.selected) {
                setIsSelected(item.selected);
            }
        }, []);

        const handleClick = () => {
            setIsSelected(!isSelected);
            if (item.selected) {
                item.selected = !item.selected;
            } else {
                item.selected = true;
            }
            if (props.setParentSidebarItems && props.parentSidebarItems) {
                props.setParentSidebarItems([...props.parentSidebarItems]);
            }
        };

        return (
            <ListItemButton
                className="sidebarItem"
                onClick={handleClick}
                sx={{
                    "&:hover": { backgroundColor: colors.hover + "!important" },
                    backgroundColor: isSelected ? colors.hover + "!important" : colors.primary + "!important",
                    paddingLeft: props.isChild ? (20 * props.lv).toString() + "%" : null,
                }}
            >
                {item.icon ? <item.icon className="sidebarIcon" sx={{ paddingRight: "3%" }} /> : null}
                <ListItemText primary={item.name} />
            </ListItemButton>
        );
    };

    const MultiLevel = (item: SidebarItem<ISidebar>) => {
        const [open, setOpen] = useState<boolean>(false);

        const handleClick = () => {
            setOpen(!open);
        };

        return (
            <React.Fragment>
                <ListItemButton
                    className="sidebarItem"
                    onClick={handleClick}
                    sx={{
                        "&:hover": { backgroundColor: colors.hover },
                        paddingLeft: props.isChild ? (20 * props.lv).toString() + "%" : null,
                    }}
                >
                    {item.icon ? <item.icon className="sidebarIcon" sx={{ paddingRight: "3%" }} /> : null}
                    <ListItemText primary={item.name} />
                    {open ? <ExpandLessRoundedIcon /> : <ExpandMoreRoundedIcon />}
                </ListItemButton>
                <Collapse in={open} timeout="auto" unmountOnExit>
                    {item.children ? (
                        <ThemeProvider theme={theme}>
                            <List className="sidebarList" disablePadding>
                                {item.children.map((child, key) => (
                                    <MenuItem
                                        item={child}
                                        isChild={true}
                                        lv={props.lv + 1}
                                        key={key}
                                        setParentSidebarItems={props.setParentSidebarItems}
                                        parentSidebarItems={props.parentSidebarItems}
                                    />
                                ))}
                            </List>
                        </ThemeProvider>
                    ) : null}
                </Collapse>
            </React.Fragment>
        );
    };

    return hasChildren(props.item) ? MultiLevel(props.item) : SingleLevel(props.item);
}
