import { Fragment } from 'react';
import { classNames } from '@/utils/classNames';

interface FormProps {
  children: React.ReactNode;
  onSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
  className?: string;
}

const Form: React.FC<FormProps> = ({ children, onSubmit, className }) => {
  const classes = classNames('form', className);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit(event);
  };

  return (
    <form onSubmit={handleSubmit} className={classes}>
      {children}
    </form>
  );
};

export { Form };