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
      <SingleDetails heading={"Full Name"} text={data?.usr_name} />
      <SingleDetails heading={"cnic"} text={data?.usrcnic} />
      <SingleDetails heading={"Phone #"} text={data?.usr_phoneNo} />
      <SingleDetails heading={"Address"} text={data?.usr_address} />
      <SingleDetails heading={"Email"} text={data?.usr_email} />
      <SingleDetails heading={"Gender"} text={data?.gender} />
      <SingleDetails heading={"Institution"} text={data?.institution} />
      <SingleDetails heading={"Bio"} text={data?.usr_bio} />
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
