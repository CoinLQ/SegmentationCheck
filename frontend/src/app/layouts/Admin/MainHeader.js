import React from "react";

import {MainHeader} from "adminlte";

const {
    ControlSidebarToggle,
    Logo,
    MainSidebarToggle,
    Nav,
    Navbar,
    Menu,
    UserMenu,
    Wrapper
} = MainHeader;


class TopNavbar extends React.Component {
    render() {
        const {actions, adminlte, navbar} = this.props;
        return (
            <Wrapper>
                <Logo/>
                {navbar && <a id="HLogo" style={{padding: 0}}></a>}
                {navbar  ||
                <Navbar>
                    <MainSidebarToggle actions={actions} adminlte={adminlte}/>


                    <Menu>
                        <Nav>

                            <UserMenu actions={actions} adminlte={adminlte}/>
                            <ControlSidebarToggle actions={actions} adminlte={adminlte}/>
                        </Nav>
                    </Menu>

                </Navbar>
                }

            </Wrapper>
        );
    }
}

export default TopNavbar;
