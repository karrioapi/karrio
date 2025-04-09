import Image from "next/image";
import Link from "next/link";

export default function LaunchWeek() {
  const launchWeekArticles = [
    {
      day: "DAY 4",
      title: "Karrio automation",
      date: "March 28, 2024",
      description: "We've set the foundations for advanced logistics operation automation. Learn more about Karrio's built-in workflow engine for no-code integration and our vision beyond shipping integration.",
      image: "/launch-week/2024-03-02-automation.png",
      link: "/blog/2024-03-02-automation"
    },
    {
      day: "DAY 3",
      title: "Karrio dashboard updates",
      date: "March 27, 2024",
      description: "discover Karrio' dashboard new fresh skin. Our design mindset and direction to cater to our ICP hypothesis. What can a developer-first and technical logistics manager platform look like?",
      image: "/launch-week/2024-03-02-dashboard-updates.png",
      link: "/blog/2024-03-02-dashboard-updates"
    },
    {
      day: "DAY 2",
      title: "Carrier accounts management",
      date: "March 26, 2024",
      description: "Carrier accounts management is a core feature of Karrio. Discover our iteration of carrier connection managment, negotiated account rates and beyond.",
      image: "/launch-week/2024-03-02-carrier-connections.png",
      link: "/blog/2024-03-02-carrier-connections"
    },
    {
      day: "DAY 1",
      title: "Karrio Update 2024.2",
      date: "March 25, 2024",
      description: "An overview and highlights of new features and the leap forward with Karrio 2024.2 edition.",
      image: "/launch-week/2024-03-01-release-2024-2.png",
      link: "/blog/2024-03-01-release-2024-2"
    }
  ];

  return (
    <div className="bg-white text-foreground">
      {/* Hero Section */}
      <section className="py-16 md:py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-0 max-w-6xl text-center">
          <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-12">
            Karrio Launch Week
          </h1>

          <p className="text-lg md:text-xl text-gray-600 max-w-3xl mx-auto mb-8 leading-relaxed">
            Shipping integration is still painful and building custom logistics solutions
            with simple supply chain visibility tech is lacking.
            <br />
            With Karrio, you can extend your platform with native shipping capabilities.
            Improve merchants and customers experience on your Marketplace, eCommerce,
            ERP, WMS, OMS, 3PL and Logistics platform.
          </p>

          <h2 className="text-2xl md:text-3xl lg:text-4xl font-bold text-[#5722cc] mb-20">
            Discover the new features,<br />capabilities and resources:
          </h2>
        </div>
      </section>

      {/* Articles Section */}
      <section className="pb-16 md:pb-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-0 max-w-6xl">
          <div className="flex flex-col space-y-10">
            {launchWeekArticles.map((article, index) => (
              <div key={index} className="flex flex-col md:flex-row border border-gray-100 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
                <Link href={article.link} className="flex-none">
                  <div className="w-full md:w-[340px] h-[200px] md:h-full relative bg-[#331C80]">
                    <Image
                      src={article.image}
                      alt={article.title}
                      fill
                      className="object-cover"
                    />
                  </div>
                </Link>
                <div className="flex flex-col p-8">
                  <div className="mb-3">
                    <span className="text-[#5722cc] text-sm font-semibold mr-3">{article.day}</span>
                    <span className="text-gray-500 text-sm">{article.date}</span>
                  </div>
                  <Link href={article.link}>
                    <h2 className="text-2xl md:text-3xl font-bold mb-3 hover:text-[#5722cc] transition-colors">
                      {article.title}
                    </h2>
                  </Link>
                  <p className="text-gray-600 mb-5 text-base leading-relaxed">
                    {article.description}
                  </p>
                  <div>
                    <Link
                      href={article.link}
                      className="text-[#5722cc] font-semibold hover:underline"
                    >
                      Read more
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
