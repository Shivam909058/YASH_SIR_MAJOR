import React from "react";
import { styled } from "@mui/material/styles";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import AccountCircle from "@mui/icons-material/AccountCircle";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Button from "@mui/material/Button";
import "./TwitterForm.css";

const StyledForm = styled('form')({ 
  display: 'flex',
  flexDirection: 'row',
  margin: '0 10%',
  border: '1px solid',
  borderRadius: '4px',
  padding: '10px',
});

const TwitterForm = ({ submit_func }) => {
  const [state, setState] = React.useState({
    tweets: true,
    retweets: false
  });

  const handleCheckChange = (event) => {
    setState({ ...state, [event.target.name]: event.target.checked });
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    const data = {
      username: e.target[0].value,
      tweets: state.tweets,
      retweets: state.retweets
    };
    submit_func(data);
  };

  return (
    <div>
      <StyledForm onSubmit={handleFormSubmit}>
        <div className="form_search_bar">
          <Grid container spacing={1} alignItems="flex-end">
            <Grid item>
              <AccountCircle />
            </Grid>
            <Grid item>
              <TextField id="input-with-icon-grid" label="Twitter Handle" />
            </Grid>
          </Grid>
        </div>
        <div className="form_check_boxes">
          <FormControlLabel
            control={
              <Checkbox
                checked={state.tweets}
                onChange={handleCheckChange}
                name="tweets"
                color="primary"
              />
            }
            label="Tweets"
          />
          <FormControlLabel
            control={
              <Checkbox
                checked={state.retweets}
                onChange={handleCheckChange}
                name="retweets"
                color="primary"
              />
            }
            label="Retweets"
          />
        </div>
        <Button
          type="submit"
          className="submit_bttn"
          variant="contained"
          color="primary"
        >
          Search
        </Button>
      </StyledForm>
    </div>
  );
};

export default TwitterForm;
