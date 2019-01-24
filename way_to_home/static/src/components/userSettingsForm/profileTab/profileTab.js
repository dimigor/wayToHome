import React from 'react';

import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Modal from '@material-ui/core/Modal';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import SettingsIcon from '@material-ui/icons/Settings';

import axios from 'axios';

import AdvancedSettings from './advancedSettings/advancedSettings.js'
import './profileTab.css';

let savedState = {
    first_name: '',
    last_name: '',
    phone_number: '',
    save_disabled: true,
    initial_first_name: '',
    initial_last_name: '',
    initial_phone_number: '',
    phone_error: false,
    email: '',
    openAdvancedModal: false,
};

export const url = '/api/v1/user';

class ProfileTab extends React.Component {
    state = {
        first_name: '',
        last_name: '',
        phone_number: '',
        save_disabled: true,
        initial_first_name: '',
        initial_last_name: '',
        initial_phone_number: '',
        phone_error: false,
        email: '',
        openAdvancedModal: false,
    };



    getProfile = () => {
        let uri = '/profile';
        axios.get(url + uri)
            .then(response => {
                this.setState({
                    first_name: response.data.first_name,
                    last_name: response.data.last_name,
                    initial_first_name: response.data.first_name,
                    initial_last_name: response.data.last_name,
                });
            })
            .catch(error => {
                console.log(error);
            })
    };

    getUserData = () => {
        axios.get(url +'/')
            .then(response => {
                this.setState({
                    phone_number: response.data.phone_number,
                    initial_phone_number: response.data.phone_number,
                    email: response.data.email,
                });
            })
            .catch(error => {
                console.log(error);
            })
    };

    saveProfile = () => {
        let uri = '/profile';
        axios.put(url + uri, {
            first_name: this.state.first_name,
            last_name: this.state.last_name,
        })
            .then(response => {
                console.log(response);
            })
            .catch(error => {
                console.log(error);
            })
    };

    savePhone = () => {
        let uri = '/phone';
        axios.put(url + uri, {
            phone: this.state.phone_number,
        })
            .then(response => {
                console.log(response);
            })
            .catch(error => {
                console.log(error);
            })
    };

    saveToDatabase = (event) => {
         this.saveProfile();
         this.savePhone();
         this.setState({
            save_disabled: true,
         });
    };

    componentDidMount(){
        if(savedState.save_disabled==true && savedState.phone_error==false){
            this.getProfile();
            this.getUserData();
        } else {
            this.setState(state=>savedState);
        }

    };

    componentWillUnmount(){
        savedState = this.state;
    };

    textFieldChangeFirstName = (event) => {
        let checked = event.target.value;
        this.setState({first_name: checked})

        if (checked !== this.state.initial_first_name){
            this.setState({save_disabled: false});
        }
        else if(this.state.last_name == this.state.initial_last_name &&
        this.state.last_name == this.state.initial_last_name){
            this.setState({save_disabled: true});
        }
    };

    textFieldChangeLastName = (event) => {
        let checked = event.target.value;
        this.setState({last_name: checked})

        if (checked != this.state.initial_last_name){
            this.setState({save_disabled: false});
        } else if (this.state.first_name == this.state.initial_first_name &&
        this.state.phone_number == this.state.initial_phone_number) {
            this.setState({save_disabled: true});
        }
    };

    textFieldChangePhoneNumber = (event) => {
        let checked = event.target.value;
        let phone_error = this.handlePhoneNumber(checked);
        this.setState({
            phone_number: checked,
            phone_error: phone_error,
        });


        if (phone_error){
            this.setState({save_disabled: true});
        } else if (checked != this.state.initial_phone_number){
            this.setState({save_disabled: false});
        } else if ((this.state.first_name == this.state.initial_first_name &&
         this.state.last_name == this.state.initial_last_name) ) {
            this.setState({save_disabled: true});
        }
    };

    handlePhoneNumber = (phone) => {
        let regex = /^\+380[0-9]{9}$/;
        return !regex.test(String(phone).toLowerCase());
    };

    onClickAdvancedBtn = () => {
        this.setState({openAdvancedModal: true});
    };


    modalAdvancedClose = () => {
        this.setState({openAdvancedModal: false});
    };

    render(){
        return(
            <div className="profileTabDiv">
                <TextField
                    className="emailField"
                    variant="outlined"
                    value={this.state.email}
                    disabled={true}
                />

                <div className="profileFields">
                    <TextField
                        label="Ім'я"
                        margin="normal"
                        variant="filled"
                        value={this.state.first_name}
                        onChange={this.textFieldChangeFirstName}
                    />
                </div>

                <div className="profileFields">
                    <TextField
                        label="Прізвіще"
                        margin="normal"
                        variant="filled"
                        value={this.state.last_name}
                        onChange={this.textFieldChangeLastName}
                    />
                </div>

                <div className="profileFields">
                    <TextField
                        label={this.state.phone_error? "Некоректний номер" : "Номер телефону"}
                        margin="normal"
                        variant="filled"
                        value={this.state.phone_number || "+380"}
                        onChange={this.textFieldChangePhoneNumber}
                        error={this.state.phone_error}
                    />
                </div>

                <Button
                    className="saveButton"
                    variant="contained"
                    color="primary"
                    size="large"
                    disabled={this.state.save_disabled}
                    onClick={this.saveToDatabase}>
                    Зберегти
                </Button>

                <Tooltip title="Додаткові Налаштування">
                    <IconButton
                    color="primary"
                    aria-label="Додаткові Налаштування"
                    onClick={this.onClickAdvancedBtn}
                    size = "medium"
                    >
                        <SettingsIcon />
                    </IconButton>
                </Tooltip>

                <div>
                    <Modal
                        open={this.state.openAdvancedModal}
                        onClose={this.modalAdvancedClose}
                        disableAutoFocus={true}>
                        <AdvancedSettings
                            close = {this.modalAdvancedClose}
                        />
                    </Modal>
                </div>


            </div>
            )
        }
}

export default ProfileTab;