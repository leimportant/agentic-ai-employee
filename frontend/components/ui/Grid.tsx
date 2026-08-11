import { Fragment } from 'react';
import { classNames } from '@/utils/classNames';

interface GridProps {
  children: React.ReactNode;
  columns?: number;
  gap?: number;
  className?: string;
}

const Grid: React.FC<GridProps> = ({
  children,
  columns = 1,
  gap = 4,
  className,
}) => {
  const classes = classNames(
    'grid',
    `grid-cols-${columns}`,
    `gap-${gap}`,
    className
  );

  return (
    <div className={classes}>
      {children}
    </div>
  );
};

export { Grid };