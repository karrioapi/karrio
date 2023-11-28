import { KARRIO_API } from "@karrio/hooks/karrio";
import { loadAPIMetadata } from "@/context/main";
import { KarrioClient } from "@karrio/types";
import { url$, logger } from "@karrio/lib";
import { GetServerSideProps } from "next";


export const getServerSideProps: GetServerSideProps = async (ctx) => {
  const { res, params } = ctx;
  const id = params?.id as string;
  const metadata = await loadAPIMetadata(ctx).catch(_ => _);
  const client = new KarrioClient({ basePath: url$`${metadata.metadata?.HOST || KARRIO_API}` });

  try {
    // Retrieve tracker by id
    const data = await client.trackers.retrieves({ idOrTrackingNumber: id })
      .then(({ data }) => ({ tracker: JSON.parse(JSON.stringify(data)) }))
      .catch(_ => {
        console.log(_.response?.data?.errors || _.response)
        return ({ message: `No Tracker ID nor Tracking Number found for ${id}` });
      });

    res.setHeader('Cache-Control', 'public, s-maxage=10, stale-while-revalidate=59')

    return { props: { id, ...metadata, ...data } };
  } catch (e) {
    logger.error(e, "Failed to retrieve tracking info");
    return { props: { id, ...metadata, ...(e as {}) } };
  }
};
