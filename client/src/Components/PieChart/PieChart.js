import React, { useEffect } from "react";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

const PieChart = ({ total_hate_speech, total_tweets }) => {
  const data = {
    labels: ['Hate Speech', 'Tweets'],
    datasets: [
      {
        data: [total_hate_speech, total_tweets],
        backgroundColor: [
          'rgba(0,123,255,0.9)',
          'rgba(0,123,255,0.5)'
        ],
        borderColor: [
          'rgba(0,123,255,1)',
          'rgba(0,123,255,1)'
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 25,
          boxWidth: 20
        }
      }
    }
  };

  return <Pie data={data} options={options} />;
};

export default PieChart;
