import React from "react";
import { BarChart, Bar, ResponsiveContainer, XAxis, Tooltip } from "recharts";

const data = [
  {
    name: "1 ☆",
    star: 5,
  },
  {
    name: "2 ☆",
    star: 4,
  },
  {
    name: "3 ☆",
    star: 3,
  },
  {
    name: "4 ☆",
    star: 2,
  },
  {
    name: "5 ☆",
    star: 1,
  },
];

const PackageRatingGraph = () => {
  return (
    <BarChart width={600} height={500} data={data}>
      <XAxis dataKey="name" />
      <Bar dataKey="star" fill="#8884d8" />
      <Tooltip />
    </BarChart>
  );
};

export default PackageRatingGraph;
