function Header() {
  return (
    <header className="w-full bg-primary p-4">
      <div className="flex items-center justify-between">
      <span className="text-2xl text-white font-medium">SGK Compliance Verification Tool</span>
      <img src="/sabanci.svg" alt="Logo" className="h-12 inline-block mr-4" />
      </div>
    </header>
  );
}

export default Header;
