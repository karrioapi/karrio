import {
  Body,
  Button,
  Container,
  Head,
  Heading,
  Html,
  Link,
  Preview,
  Section,
  Text,
} from "@react-email/components";

interface InviteEmailProps {
  inviteUrl: string;
  organizationName: string;
  inviterName: string;
}

export function InviteEmail({
  inviteUrl,
  organizationName,
  inviterName,
}: InviteEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>Join {organizationName} on Karrio</Preview>
      <Body style={{ backgroundColor: "#f6f9fc", padding: "40px 0" }}>
        <Container>
          <Heading>Join {organizationName} on Karrio</Heading>
          <Section>
            <Text>
              {inviterName} has invited you to join their organization on
              Karrio.
            </Text>
            <Button href={inviteUrl} style={{ background: "#7c3aed" }}>
              Accept Invitation
            </Button>
            <Text style={{ color: "#667" }}>
              or copy and paste this URL into your browser:{" "}
              <Link href={inviteUrl}>{inviteUrl}</Link>
            </Text>
          </Section>
        </Container>
      </Body>
    </Html>
  );
}
