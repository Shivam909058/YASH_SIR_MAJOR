import React, { useEffect, useState } from "react";
import { styled } from "@mui/material/styles";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  "&:nth-of-type(odd)": {
    backgroundColor: theme.palette.action.hover,
  },
}));

const DataTable = ({ data }) => {
  const [tdata, setTdata] = useState([]);

  useEffect(() => {
    const hate_speech_arr = data
      .filter(obj => obj.isHateSpeech === "1")
      .map(obj => obj.text);
    setTdata(hate_speech_arr);
  }, [data]);

  if (!tdata.length) return null;

  return (
    <TableContainer component={Paper}>
      <Table aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell align="right">Sno</StyledTableCell>
            <StyledTableCell align="right">Potential Hate Speech Tweet</StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {tdata.map((row, idx) => (
            <StyledTableRow key={idx}>
              <StyledTableCell align="right">{idx}</StyledTableCell>
              <StyledTableCell align="right">{row}</StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default DataTable;
