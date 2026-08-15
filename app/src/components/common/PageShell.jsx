import { NavLink } from "react-router-dom";

const NAV_ITEMS = [
  { label: "Overview", to: "/" },
  { label: "Market Research", to: "/market-research" },
  { label: "SWOT Analysis", to: "/swot-analysis" },
  { label: "Marketing Plan", to: "/marketing-plan" },
];

function PageShell({ title, subtitle, children }) {
  return (
    <div className="layout">
      <header className="masthead">
        <div className="brand-block">
          <p className="eyebrow">CoFounder AI</p>
          <h1>{title}</h1>
          <p className="subtitle">{subtitle}</p>
        </div>
        <nav className="topnav" aria-label="Main navigation">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => `navlink ${isActive ? "navlink-active" : ""}`.trim()}
              end={item.to === "/"}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </header>
      <main>{children}</main>
    </div>
  );
}

export default PageShell;
