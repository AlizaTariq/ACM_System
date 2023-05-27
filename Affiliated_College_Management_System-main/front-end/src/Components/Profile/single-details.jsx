import React from "react";

const SingleDetails = ({ heading, text, border = true }) => {
  return (
    <div
      className={`row py-3 ${border && "border-bottom"} `}
      style={{ borderColor: "#e0e0e0" }}
    >
      <div className="col-md-3 col-12">
        <h4 className="heading-4 text-left">{heading}</h4>
      </div>
      <div className="col-md-8 col-12">
        <h4 className="heading-6 text-left text-secondary">{text}</h4>
      </div>
    </div>
  );
};

export default SingleDetails;
