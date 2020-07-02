import React, { Component } from "react";
import { connect } from 'react-redux';
import { Route, BrowserRouter as Router, Link } from "react-router-dom";

// import Button from 'react-bootstrap/Button';
import { Button, Form } from "react-bootstrap";
const axios = require('axios');

class UpdateUser extends Component {

    updateUser() {
        let user = axios.put('http://localhost:5000/users/updateUser', {
            username: this.props.username,
            password: this.props.password,
            updateUsername: this.props.updateUsername,
            updatePassword: this.props.updatePassword,
            updateDpt: this.props.updateDpt,
            updateFuncTeam: this.props.FuncTeam,
            updateTitle: this.props.updateTitle
        })
        this.props.handleUserUpdate(user);

    }


    render() {
        return (
            <>
                <div className="Update" style={{ width: '30%', height: 'auto', margin: 'auto' }}>
                    <h1 style={{ textAlign: 'center' }}>UPDATE USER INFO</h1>
                    <br></br>
                        <label>
                            Username
                <input className="form-control" type="text" name="username" placeholder={this.props.user.username}
                                value={this.props.updateUsername}
                                onChange={this.props.handleUpdateUsernameInput} />
                        </label>
                        <label for="password">
                            Password
                <input className="form-control" type="password" name="password" placeholder={this.props.user.password}
                                value={this.props.updatePassword}
                                onChange={this.props.handleUpdatePasswordInput} />
                        </label>
                        <label for="department">
                            Department
                <input className="form-control" type="text" name="department" placeholder={this.props.user.department}
                                value={this.props.updateDpt}
                                onChange={this.props.handleUpdateDepartmentInput} />
                        </label>
                        <label for="functional_team">
                            Functional Team
                <input className="form-control" type="text" name="functional_team" placeholder={this.props.user.functional_team}
                                value={this.props.updateFuncTeam}
                                onChange={this.props.handleUpdateFuncTeamInput} />
                        </label>
                        <label for="title">
                            Title
                <input className="form-control" type="text" name="title" placeholder={this.props.user.title}
                                value={this.props.updateTitle}
                                onChange={this.props.handleUpdateTitleInput} />
                        </label>
                        <br></br>
                        <Button onClick={() => this.updateUser()}>Submit</Button>
                    </div>
            </>
        )
    }
}

function mapStateToProps(state) {
    const { user, username, password, updateUsername, updatePassword, updateDpt, updateFuncTeam, updateTitle } = state;
    return {
        user: user,
        username: username,
        password: password,
        updateUsername: updateUsername,
        updatePassword: updatePassword,
        updateDpt: updateDpt,
        updateFuncTeam: updateFuncTeam,
        updateTitle: updateTitle
    }
}

function mapDispatchToProps(dispatch) {
    return {
        handleUpdateUsernameInput: (e) => dispatch({ type: 'handleUpdateUsername', updateUsername: e.target.value }),
        handleUpdatePasswordInput: (e) => dispatch({ type: 'handleUpdatePassword', updatePassword: e.target.value }),
        handleUpdateDepartmentInput: (e) => dispatch({ type: 'handleUpdateDepartment', updateDpt: e.target.value }),
        handleUpdateFuncTeamInput: (e) => dispatch({ type: 'handleUpdateFuncTeam', updateFuncTeam: e.target.value }),
        handleUpdateTitleInput: (e) => dispatch({ type: 'handleUpdateTitle', updateTitle: e.target.value }),
        handleUserUpdate: (user) => dispatch({ type: 'updateUser', user: user })
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(UpdateUser);
