import Image from "next/image";
import Link from "next/link";

interface KarrioLogoProps {
  className?: string;
}

export function KarrioLogo({ className }: KarrioLogoProps) {
  return (
    <Link href="/orgs" className={className}>
      <Image
        src="/icon.svg"
        alt="Karrio Logo"
        width={24}
        height={24}
        className="h-6 w-6"
      />
    </Link>
  );
}
