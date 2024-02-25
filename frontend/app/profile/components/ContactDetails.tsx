import React from "react";
import { DetailField } from "./DetailField";

export default function ContactDetails() {
  const phoneNum = "123-456-7890";
  const email = "john.doe@email.com";
  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-xl font-medium">Contact Details</h1>
      <div className="flex flex-col gap-4 text-black dark:text-white">
        <DetailField title={"phoneNum"} value={phoneNum} />
        <DetailField title={"email"} value={email} />
      </div>
    </div>
  );
}
