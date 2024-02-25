import React from "react";
import Image from "next/image";
import { DetailField } from "./DetailField";
export default function PersonalDetails() {
  const name = "John Doe";
  const city = "Calgary";
  const state = "Alberta";

  return (
    <div className="flex flex-col gap-4 ">
      <h1 className="text-xl font-medium">Personal Details</h1>
      <div className="flex flex-row gap-4">
        <Image
          src="/missingImage.jpg"
          alt="profileImage"
          width={180}
          height={200}
          className="rounded-xl object-fill shadow-lg"
        />
        <div className="flex flex-col gap-4 text-black dark:text-white">
          <DetailField title={"Name"} value={name} />
          <DetailField title={"Gender"} value={"Female"} />
          <DetailField title={"City"} value={city} />
          <DetailField title={"State"} value={state} />
        </div>
      </div>
    </div>
  );
}
