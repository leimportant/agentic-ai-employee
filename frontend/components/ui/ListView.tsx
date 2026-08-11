import { Fragment } from 'react';
import { classNames } from '@/utils/classNames';

interface ListViewProps {
  children: React.ReactNode;
  className?: string;
}

const ListView: React.FC<ListViewProps> = ({ children, className }) => {
  const classes = classNames('list-view', className);

  return (
    <ul className={classes}>
      {children}
    </ul>
  );
};

export { ListView };