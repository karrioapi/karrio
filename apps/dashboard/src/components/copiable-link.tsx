import React from 'react';

interface CopiableLinkComponent extends React.InputHTMLAttributes<HTMLAnchorElement> {
  text: string;
  value?: string;
}

const CopiableLink: React.FC<CopiableLinkComponent> = ({ text, value, className, style, ...props }) => {
  const copyText = (_: React.MouseEvent) => {
    var input = document.createElement('input');
    input.setAttribute('value', value || text);
    document.body.appendChild(input);
    input.select();
    document.execCommand('copy');
    document.body.removeChild(input);
  };

  return (
    <a
      className={className || "button is-white is-small m-1"}
      style={style || { padding: '0', height: '20px' }}
      onClick={copyText}
      {...props}>
      <span>{text}</span>
      <i className="fas fa-clipboard ml-3"></i>
    </a>
  )
};

export default CopiableLink;
