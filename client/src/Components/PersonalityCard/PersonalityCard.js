import React from "react";
import { styled } from "@mui/material/styles";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";

const StyledCard = styled(Card)(({ theme }) => ({
  maxWidth: 445,
  marginLeft: "30px"
}));

const PersonalityCard = ({ type }) => {
  function get_full_form(type) {
    let ans = "";
    for (let i = 0; i < 4; i++) {
      const text = type[i];
      switch (text) {
        case "I": ans += "INTROVERT "; break;
        case "E": ans += "EXTROVERT "; break;
        case "N": ans += "INTUTIVE "; break;
        case "S": ans += "SENSING "; break;
        case "T": ans += "THINKING "; break;
        case "J": ans += "JUDGING "; break;
        case "F": ans += "FEELING "; break;
        case "P": ans += "PERCEIVING "; break;
        default: ans += ""; break;
      }
    }
    return ans.trim();
  }

  return (
    <StyledCard>
      <CardContent>
        <Typography gutterBottom variant="h5" component="h2">
          {type}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {get_full_form(type)}
        </Typography>
      </CardContent>
    </StyledCard>
  );
};

export default PersonalityCard;
