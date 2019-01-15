import {Component, Fragment} from "react";
import TextField from '@material-ui/core/TextField';
import React from "react";

export default class InputPoint extends Component {

  handleChange = event => {
      let value = event.target.value;
      if (value.length > 3) {
          this.props.onChange(value)
      }
  }

    render(){

      return (
        <Fragment>
          <TextField
            label={this.props.name}
            value={this.props.value}
            InputLabelProps={{ shrink: true }}
            onChange={this.handleChange}/>
        </Fragment>
      )
    }
};