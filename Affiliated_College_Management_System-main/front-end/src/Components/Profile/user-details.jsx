import React from "react";
import SingleDetails from "./single-details";

const data = [
  {
    fullName: "John Doe",
    cnic: "35202-0000000-0",
  },
];

const UserDetails = ({ data }) => {
  return (
    <div className="p-3 ">
      <SingleDetails heading={"Full Name"} text={data?.name} />
      <SingleDetails heading={"cnic"} text={data?.cnic} />
      <SingleDetails heading={"Phone #"} text={data?.phone} />
      <SingleDetails heading={"Address"} text={data?.address} />
      <SingleDetails heading={"Email"} text={data?.email} />
      <SingleDetails heading={"Gender"} text={data?.gender} />
      <SingleDetails heading={"Institution"} text={data?.institution} />
      <SingleDetails heading={"Bio"} text={data?.bio} />
      <SingleDetails heading={"Ranking"} text={data?.ranking} />
      <SingleDetails
        heading={"Acceptance Count"}
        text={data?.acceptance_count}
      />
      <SingleDetails
        heading={"Rejection Count"}
        text={data?.rejection_count}
        border={false}
      />
    </div>
  );
};

export default UserDetails;
