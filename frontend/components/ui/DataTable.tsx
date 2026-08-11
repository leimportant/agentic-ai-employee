import { Fragment } from 'react';
import { classNames } from '@/utils/classNames';

interface DataTableProps {
  children: React.ReactNode;
  className?: string;
}

const DataTable: React.FC<DataTableProps> = ({ children, className }) => {
  const classes = classNames('data-table', className);

  return (
    <table className={classes}>
      {children}
    </table>
  );
};

export { DataTable };