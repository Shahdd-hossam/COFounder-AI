import { NavLink } from "react-router-dom";

const NAV_ITEMS = [
  { label: "Home", to: "/" },
  { label: "Marketing Plan", to: "/marketing-plan" },
  { label: "Market Research", to: "/market-research" },
  { label: "SWOT", to: "/swot-analysis" },
];

function PageShell({ title, subtitle, children }) {
  return (
    <div className="layout">
      <header className="masthead">
        <div>
          <p className="eyebrow">Marketing AI Studio</p>
          <h1>{title}</h1>
          <p className="subtitle">{subtitle}</p>
        </div>
        <nav className="topnav" aria-label="Main Navigation">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `navlink ${isActive ? "navlink-active" : ""}`.trim()
              }
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
