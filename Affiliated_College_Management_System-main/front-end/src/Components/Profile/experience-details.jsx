import React from "react";
import SingleDetailsV2 from "./single-details-v2";

const ExperienceDetails = ({ data }) => {
  return (
    <div className="p-3 ">
      <SingleDetailsV2 heading={"Job Title"} text={data?.job_title} />
      <SingleDetailsV2
        heading={"Organization Name"}
        text={data?.organization_name}
      />
      <SingleDetailsV2
        heading={"Reference Email"}
        text={data?.reference_email}
      />
      <SingleDetailsV2 heading={"Starting Date"} text={data?.starting_date} />
      <SingleDetailsV2 heading={"Ending Date"} text={data?.ending_date} />
      <SingleDetailsV2
        heading={"Experience latter"}
        text={data?.experience_latter ? "" : "N/A"}
        file={data?.experience_latter?.length > 0 ? true : false}
      />
    </div>
  );
};

export default ExperienceDetails;
