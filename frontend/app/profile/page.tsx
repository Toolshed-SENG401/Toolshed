import React from "react";
import PersonalDetails from "./components/PersonalDetails";
import ContactDetails from "./components/ContactDetails";
import Rating from "./components/Rating";
import Biography from "./components/Biography";

export default function page() {
  return (
    // TODO: responsive design
    <div className="bg-white dark:bg-black w-full p-24 rounded-xl text-brand flex flex-row justify-between">
      <PersonalDetails></PersonalDetails>
      <div className=" flex flex-col gap-8">
        <ContactDetails></ContactDetails>
        <Rating></Rating>
      </div>
      <Biography></Biography>
    </div>
  );
}
