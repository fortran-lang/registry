import React from "react";
import { BarChart, Bar, XAxis, Tooltip } from "recharts";

const PackageRatingGraph = ({ data }) => {
  const graphData = data;

  const parsedArray = Object.entries(graphData).map(([key, value]) => ({
    name: `${key} ⭐`,
    star: value,
  }));

  return (
    <BarChart width={600} height={500} data={parsedArray}>
      <XAxis dataKey="name" />
      <Bar dataKey="star" fill="#8884d8" />
      <Tooltip />
    </BarChart>
  );
};

export default PackageRatingGraph;
