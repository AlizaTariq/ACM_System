import React from "react";
import SingleDetailsV2 from "./single-details-v2";

const QualificationDetails = ({ data }) => {
  return (
    <div className="p-3 ">
      <SingleDetailsV2 heading={"Degree Title"} text={data?.degree_title} />
      <SingleDetailsV2 heading={"Institution Name"} text={data?.institution} />
      <SingleDetailsV2 heading={"Starting Date"} text={data?.starting_date} />
      <SingleDetailsV2 heading={"Ending Date"} text={data?.ending_date} />
      <SingleDetailsV2
        heading={"Transcript latter"}
        text={data?.transcript ? "" : "N/A"}
        file={data?.transcript}
      />
    </div>
  );
};

export default QualificationDetails;
