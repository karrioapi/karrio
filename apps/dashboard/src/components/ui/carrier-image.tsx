import React from 'react'
import { cn } from '@/lib/utils'

interface CarrierImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  carrierName: string
  size?: 'sm' | 'md' | 'lg'
  variant?: 'icon' | 'logo'
  fallbackColor?: string
  fallbackBackground?: string
}

const sizeMap = {
  sm: { width: 32, height: 32, text: 'text-xs' },
  md: { width: 48, height: 48, text: 'text-sm' },
  lg: { width: 64, height: 64, text: 'text-base' },
}

export function CarrierImage({
  carrierName,
  size = 'md',
  variant = 'icon',
  fallbackColor = '#ffffff',
  fallbackBackground = '#6366f1',
  className,
  ...props
}: CarrierImageProps) {
  const { width, height, text } = sizeMap[size]

  // Format carrier name for file lookup
  const formattedName = carrierName.toLowerCase().replace(/[^a-z0-9]/g, '')

  // Generate initials for fallback
  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((word) => word[0])
      .join('')
      .substring(0, 2)
      .toUpperCase()
  }

  const initials = getInitials(carrierName)

  // Create SVG fallback
  const createFallbackSvg = () => {
    const svg = `
      <svg viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">
        <rect width="${width}" height="${height}" rx="6" fill="${fallbackBackground}" />
        <text x="50%" y="50%" text-anchor="middle" dominant-baseline="middle"
              fill="${fallbackColor}" font-family="system-ui" font-weight="600"
              font-size="${Math.floor(width * 0.4)}">
          ${initials}
        </text>
      </svg>
    `
    return `data:image/svg+xml;base64,${btoa(svg)}`
  }

  const [imageError, setImageError] = React.useState(false)
  const [imageLoaded, setImageLoaded] = React.useState(false)

  const handleImageError = () => {
    setImageError(true)
  }

  const handleImageLoad = () => {
    setImageLoaded(true)
    setImageError(false)
  }

  const imagePath = `/carriers/${formattedName}_${variant}.svg`

  return (
    <div
      className={cn(
        'inline-flex items-center justify-center rounded-md bg-gray-100 overflow-hidden',
        className,
      )}
      style={{ width, height }}
    >
      {!imageError ? (
        <img
          src={imagePath}
          alt={carrierName}
          width={width}
          height={height}
          onError={handleImageError}
          onLoad={handleImageLoad}
          className={cn(
            'transition-opacity duration-200',
            imageLoaded ? 'opacity-100' : 'opacity-0',
          )}
          {...props}
        />
      ) : (
        <img
          src={createFallbackSvg()}
          alt={carrierName}
          width={width}
          height={height}
          className="rounded-md"
          {...props}
        />
      )}
    </div>
  )
}
