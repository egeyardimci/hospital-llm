function Header() {
  return (
    <header className="w-full bg-primary p-4">
      <div className="flex items-center justify-between">
        <div>
          <span className="text-2xl text-white font-bold">SGK</span>
          <span className="text-2xl text-white font-medium">
            &nbsp;Compliance Verification Tool
          </span>
        </div>
        <img src="/sabanci.svg" alt="Logo" className="h-12 inline-block mr-4" />
      </div>
    </header>
  );
}

export default Header;
