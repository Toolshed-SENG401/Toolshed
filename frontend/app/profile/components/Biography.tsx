import { Label, Textarea } from "flowbite-react";

export default function Biography() {
  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-xl font-medium">Biography</h1>
      <div className="flex flex-col gap-4 text-black dark:text-white">
        <div className="max-w-md">
          <div className="mb-2 block">
            <Label htmlFor="comment" value="Your message" />
          </div>
          <Textarea
            id="comment"
            placeholder="Enter a description..."
            required
            rows={4}
            className=" bg-purple-200 text-brand shadow "
          />
        </div>
      </div>
    </div>
  );
}
