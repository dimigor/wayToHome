import React, {Component} from 'react';

import TrendingFlat from '@material-ui/icons/TrendingFlat';
import MenuItem from '@material-ui/core/MenuItem';
import TextField from '@material-ui/core/TextField';
import DeleteIcon from '@material-ui/icons/Delete';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import SaveAlt from '@material-ui/icons/SaveAlt';

import './newWayItem.css';


export default class NewWayItem extends Component{

    state = {
        placeA: 'Виберіть місце A',
        placeB: 'Виберіть місце Б',
    };



    newWayValidator(){
        if (this.state.placeA === this.state.placeB) {
            return false
        }

        if (!Number.isInteger(this.state.placeA) || !Number.isInteger(this.state.placeB)){
            return false
        }
        return true
    }

     handleChange = name => event => {
        this.setState({
            [name]: event.target.value,
         });
     };

    render() {
        return (
            <div className="newWayItem">
                <TextField
                  select
                  className="textField"
                  label="Місце А"
                  value={this.state.placeA}
                  onChange={this.handleChange('placeA')}
                  helperText="Виберіть одне з Ваших збережених місць"
                  margin="normal"
                >
                  {this.props.places.map(place => (
                    <MenuItem key={place.id} value={place.id}>
                      {place.name}
                    </MenuItem>
                  ))}
                </TextField>

                <TrendingFlat className="arrow" />

                <TextField
                  select
                  className="textField"
                  label="Місце Б"
                  value={this.state.placeB}
                  onChange={this.handleChange('placeB')}
                  helperText="Виберіть одне з Ваших збережених місць"
                  margin="normal"
                >
                  {this.props.places.map(place => (
                    <MenuItem key={place.id} value={place.id}>
                      {place.name}
                    </MenuItem>
                  ))}
                </TextField>

                <Tooltip title="Зберегти">
                    <IconButton
                        style={this.newWayValidator()?{color: "green"}:{color: "grey"}}
                        disabled={!this.newWayValidator()}
                        aria-label="Зберегти"
                        onClick={() => this.props.saveButton(this.state.placeA, this.state.placeB)}
                    >
                        <SaveAlt />
                    </IconButton>
                </Tooltip>

                <Tooltip title="Видалити">
                    <IconButton
                        color="secondary"
                        aria-label="Видалити"
                        onClick={this.props.deleteButton}
                    >
                        <DeleteIcon />
                    </IconButton>
                </Tooltip>

            </div>
        )
    }
}