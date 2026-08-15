import { render, screen } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import App from "./App";

test("renders the CoFounder AI overview", () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>,
  );
  expect(screen.getByRole("heading", { name: "CoFounder AI" })).toBeTruthy();
  expect(screen.getByText("Create startup")).toBeTruthy();
});
