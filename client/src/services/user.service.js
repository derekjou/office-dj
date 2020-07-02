const { default: axios } = require('axios')

class UserService {
    constructor(){
        this.URI = 'http://localhost:5000/users';
    }

    login(username, password) {
        return axios({
            method: 'POST',
            url: `${this.URI}/login`,
            data: {
                username: username, 
                password: password, 
            },
            withCredentials: true
        })
    }

    updateUser(username, password, department, team, title) {
        return axios({
            method: 'PUT',
            url: `${this.URI}/updateUser`,
            data: {
                user_name: username, 
                password: password, 
                department: department, 
                functional_team: team, 
                title: title
            },
            withCredentials: true
        })
    }
}

export default UserService;