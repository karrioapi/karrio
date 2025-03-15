import { useLocation } from '@docusaurus/router';
import { useEffect, useState } from 'react';

export function usePlatformColorMode() {
    const location = useLocation();
    const [isPlatformTheme, setIsPlatformTheme] = useState(false);

    useEffect(() => {
        // Check if current page is platform related
        const isPlatform = location.pathname.startsWith('/platform');
        setIsPlatformTheme(isPlatform);
    }, [location]);

    return { isPlatformTheme };
}
